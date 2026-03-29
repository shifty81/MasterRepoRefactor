"""AtlasAI Phase 26B — Behavior Tree Compiler.

Parses, validates, and compiles visual behavior tree definitions into an
optimised flat-array bytecode representation for efficient runtime evaluation
by the AI execution engine.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class BTNodeDef:
    """Source definition for a single behavior tree node."""

    node_id: str
    node_type: str          # "Sequence", "Selector", "Action", "Condition", etc.
    name: str = ""
    action_id: str = ""
    condition_id: str = ""
    decorator_type: str = ""
    parallel_policy: str = "RequireAll"
    children: list[str] = field(default_factory=list)
    blackboard_key: str = ""
    blackboard_op: str = ""
    blackboard_value: str = ""
    repeat_count: int = -1
    cooldown_seconds: float = 0.0
    timeout_seconds: float = 0.0
    weight: float = 1.0
    enabled: bool = True

    @property
    def child_count(self) -> int:
        return len(self.children)

    @property
    def is_composite(self) -> bool:
        return self.node_type in ("Sequence", "Selector", "Parallel")

    @property
    def is_leaf(self) -> bool:
        return self.node_type in ("Action", "Condition", "BlackboardQuery")


@dataclass
class BTBytecodeInstruction:
    """A single compiled instruction in the flat bytecode stream."""

    opcode: str
    operand_a: str = ""
    operand_b: str = ""
    operand_c: str = ""
    jump_target: int = -1
    float_param: float = 0.0
    int_param: int = 0

    def __str__(self) -> str:
        return (
            f"{self.opcode:<20} "
            f"a={self.operand_a!r:16} "
            f"b={self.operand_b!r:16} "
            f"jmp={self.jump_target}"
        )


@dataclass
class BTCompileResult:
    """Result of compiling a single behavior tree."""

    tree_id: str
    tree_name: str
    success: bool = False
    error_message: str = ""
    warnings: list[str] = field(default_factory=list)
    instructions: list[BTBytecodeInstruction] = field(default_factory=list)
    node_count: int = 0
    instruction_count: int = 0
    compile_time_ms: float = 0.0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    @property
    def bytecode_size_bytes(self) -> int:
        return self.instruction_count * 64


@dataclass
class BTSourceTree:
    """A behavior tree source definition ready for compilation."""

    tree_id: str
    name: str
    root_node_id: str = ""
    nodes: dict[str, BTNodeDef] = field(default_factory=dict)
    blackboard_keys: list[str] = field(default_factory=list)
    version: int = 1

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    def add_node(self, node: BTNodeDef) -> None:
        self.nodes[node.node_id] = node

    def get_node(self, node_id: str) -> Optional[BTNodeDef]:
        return self.nodes.get(node_id)


class BehaviorTreeCompiler:
    """Compiles behavior tree source definitions into flat bytecode."""

    # Supported opcodes
    OPCODES = {
        "Sequence", "Selector", "Parallel",
        "Decorate", "RunAction", "CheckCondition",
        "QueryBlackboard", "CallSubTree",
        "SucceedAlways", "FailAlways",
        "RepeatN", "RetryUntilFail",
        "Cooldown", "Timeout",
        "JumpIfFail", "JumpIfSuccess", "Jump",
        "Return",
    }

    def __init__(self) -> None:
        self._source_trees: dict[str, BTSourceTree] = {}
        self._results: dict[str, BTCompileResult] = {}
        self._next_tree: int = 0
        self._next_node: int = 0

    # ------------------------------------------------------------------
    # Source tree management
    # ------------------------------------------------------------------

    def create_source_tree(self, name: str) -> BTSourceTree:
        tree_id = f"tree_{self._next_tree:04d}"
        self._next_tree += 1
        tree = BTSourceTree(tree_id=tree_id, name=name)
        self._source_trees[tree_id] = tree
        logger.debug("Created source tree %s", tree_id)
        return tree

    def get_source_tree(self, tree_id: str) -> Optional[BTSourceTree]:
        return self._source_trees.get(tree_id)

    def get_source_tree_count(self) -> int:
        return len(self._source_trees)

    def get_all_tree_ids(self) -> list[str]:
        return list(self._source_trees.keys())

    def remove_source_tree(self, tree_id: str) -> bool:
        if tree_id not in self._source_trees:
            return False
        del self._source_trees[tree_id]
        self._results.pop(tree_id, None)
        return True

    # ------------------------------------------------------------------
    # Node management
    # ------------------------------------------------------------------

    def add_node(
        self,
        tree_id: str,
        node_type: str,
        name: str = "",
        action_id: str = "",
        condition_id: str = "",
    ) -> Optional[BTNodeDef]:
        tree = self._source_trees.get(tree_id)
        if tree is None:
            return None
        node_id = f"node_{self._next_node:05d}"
        self._next_node += 1
        node = BTNodeDef(
            node_id=node_id,
            node_type=node_type,
            name=name or node_type,
            action_id=action_id,
            condition_id=condition_id,
        )
        tree.add_node(node)
        if not tree.root_node_id:
            tree.root_node_id = node_id
        return node

    def add_child(self, tree_id: str, parent_id: str, child_id: str) -> bool:
        tree = self._source_trees.get(tree_id)
        if tree is None:
            return False
        parent = tree.get_node(parent_id)
        if parent is None or child_id not in tree.nodes:
            return False
        if child_id not in parent.children:
            parent.children.append(child_id)
        return True

    def set_root(self, tree_id: str, node_id: str) -> bool:
        tree = self._source_trees.get(tree_id)
        if tree is None or node_id not in tree.nodes:
            return False
        tree.root_node_id = node_id
        return True

    def add_blackboard_key(self, tree_id: str, key: str) -> bool:
        tree = self._source_trees.get(tree_id)
        if tree is None:
            return False
        if key not in tree.blackboard_keys:
            tree.blackboard_keys.append(key)
        return True

    def get_node_count(self, tree_id: str) -> int:
        tree = self._source_trees.get(tree_id)
        return tree.node_count if tree else 0

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self, tree_id: str) -> list[str]:
        """Returns a list of validation error messages (empty = valid)."""
        errors: list[str] = []
        tree = self._source_trees.get(tree_id)
        if tree is None:
            return [f"Tree {tree_id} not found"]
        if not tree.root_node_id:
            errors.append("Tree has no root node")
        if tree.root_node_id and tree.root_node_id not in tree.nodes:
            errors.append(f"Root node {tree.root_node_id!r} does not exist")
        for node_id, node in tree.nodes.items():
            for child_id in node.children:
                if child_id not in tree.nodes:
                    errors.append(
                        f"Node {node_id!r} references unknown child {child_id!r}"
                    )
            if node.node_type == "Action" and not node.action_id:
                errors.append(f"Action node {node_id!r} has no action_id")
            if node.node_type == "Condition" and not node.condition_id:
                errors.append(f"Condition node {node_id!r} has no condition_id")
        return errors

    # ------------------------------------------------------------------
    # Compilation
    # ------------------------------------------------------------------

    def compile(self, tree_id: str) -> BTCompileResult:
        import time
        start = time.time()
        tree = self._source_trees.get(tree_id)
        if tree is None:
            result = BTCompileResult(
                tree_id=tree_id,
                tree_name="",
                success=False,
                error_message=f"Tree {tree_id} not found",
            )
            self._results[tree_id] = result
            return result

        errors = self.validate(tree_id)
        result = BTCompileResult(
            tree_id=tree_id,
            tree_name=tree.name,
            node_count=tree.node_count,
        )

        if errors:
            result.success = False
            result.error_message = "; ".join(errors)
            self._results[tree_id] = result
            return result

        instructions = self._emit_instructions(tree)
        result.instructions = instructions
        result.instruction_count = len(instructions)
        result.success = True
        result.compile_time_ms = (time.time() - start) * 1000

        if tree.node_count == 0:
            result.warnings.append("Tree has no nodes")

        self._results[tree_id] = result
        return result

    def compile_all(self) -> list[BTCompileResult]:
        return [self.compile(tree_id) for tree_id in self._source_trees]

    def _emit_instructions(
        self, tree: BTSourceTree
    ) -> list[BTBytecodeInstruction]:
        instructions: list[BTBytecodeInstruction] = []
        if tree.root_node_id and tree.root_node_id in tree.nodes:
            self._emit_node(tree, tree.root_node_id, instructions)
        instructions.append(BTBytecodeInstruction(opcode="Return"))
        return instructions

    def _emit_node(
        self,
        tree: BTSourceTree,
        node_id: str,
        instructions: list[BTBytecodeInstruction],
    ) -> None:
        node = tree.nodes.get(node_id)
        if node is None or not node.enabled:
            return

        if node.node_type == "Action":
            instructions.append(
                BTBytecodeInstruction(
                    opcode="RunAction",
                    operand_a=node.action_id,
                    operand_b=node.node_id,
                )
            )
        elif node.node_type == "Condition":
            instructions.append(
                BTBytecodeInstruction(
                    opcode="CheckCondition",
                    operand_a=node.condition_id,
                    operand_b=node.node_id,
                )
            )
        elif node.node_type == "Sequence":
            instructions.append(
                BTBytecodeInstruction(opcode="Sequence", operand_a=node.node_id,
                                       int_param=node.child_count)
            )
            for child_id in node.children:
                self._emit_node(tree, child_id, instructions)
        elif node.node_type == "Selector":
            instructions.append(
                BTBytecodeInstruction(opcode="Selector", operand_a=node.node_id,
                                       int_param=node.child_count)
            )
            for child_id in node.children:
                self._emit_node(tree, child_id, instructions)
        elif node.node_type == "Parallel":
            instructions.append(
                BTBytecodeInstruction(
                    opcode="Parallel",
                    operand_a=node.node_id,
                    operand_b=node.parallel_policy,
                    int_param=node.child_count,
                )
            )
            for child_id in node.children:
                self._emit_node(tree, child_id, instructions)
        elif node.node_type == "Decorator":
            instructions.append(
                BTBytecodeInstruction(
                    opcode="Decorate",
                    operand_a=node.decorator_type,
                    operand_b=node.node_id,
                    float_param=node.cooldown_seconds,
                )
            )
            for child_id in node.children:
                self._emit_node(tree, child_id, instructions)
        elif node.node_type == "BlackboardQuery":
            instructions.append(
                BTBytecodeInstruction(
                    opcode="QueryBlackboard",
                    operand_a=node.blackboard_key,
                    operand_b=node.blackboard_op,
                    operand_c=node.blackboard_value,
                )
            )
        elif node.node_type == "SubTree":
            instructions.append(
                BTBytecodeInstruction(
                    opcode="CallSubTree",
                    operand_a=node.action_id,
                    operand_b=node.node_id,
                )
            )

    # ------------------------------------------------------------------
    # Result access
    # ------------------------------------------------------------------

    def get_result(self, tree_id: str) -> Optional[BTCompileResult]:
        return self._results.get(tree_id)

    def get_result_count(self) -> int:
        return len(self._results)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_bytecode(self, tree_id: str, output_path: str) -> bool:
        result = self._results.get(tree_id)
        if result is None or not result.success:
            return False
        data = {
            "tree_id": result.tree_id,
            "tree_name": result.tree_name,
            "instruction_count": result.instruction_count,
            "bytecode_size_bytes": result.bytecode_size_bytes,
            "instructions": [
                {
                    "opcode": ins.opcode,
                    "operand_a": ins.operand_a,
                    "operand_b": ins.operand_b,
                    "jump_target": ins.jump_target,
                    "float_param": ins.float_param,
                    "int_param": ins.int_param,
                }
                for ins in result.instructions
            ],
        }
        try:
            Path(output_path).write_text(json.dumps(data, indent=2))
            return True
        except OSError as exc:
            logger.error("Failed to save bytecode: %s", exc)
            return False

    def load_source_from_dict(self, data: dict) -> Optional[BTSourceTree]:
        """Load a source tree from a dict (e.g. parsed JSON)."""
        try:
            tree_id = data.get("tree_id", f"tree_{self._next_tree:04d}")
            self._next_tree += 1
            tree = BTSourceTree(
                tree_id=tree_id,
                name=data.get("name", ""),
                root_node_id=data.get("root_node_id", ""),
                blackboard_keys=data.get("blackboard_keys", []),
            )
            for nd in data.get("nodes", []):
                node = BTNodeDef(
                    node_id=nd["node_id"],
                    node_type=nd.get("node_type", "Action"),
                    name=nd.get("name", ""),
                    action_id=nd.get("action_id", ""),
                    condition_id=nd.get("condition_id", ""),
                    children=nd.get("children", []),
                )
                tree.add_node(node)
            self._source_trees[tree.tree_id] = tree
            return tree
        except (KeyError, TypeError) as exc:
            logger.error("load_source_from_dict failed: %s", exc)
            return None

    def clear(self) -> None:
        self._source_trees.clear()
        self._results.clear()
        self._next_tree = 0
        self._next_node = 0
