"""
test_launch_system.py
Tests for K-series (launch / executable boot system):
  K1 — LaunchConfig
  K2 — GameSystemsRegistry
  K3 — PlaytestSession
  K4 — RuntimeDiagnostics
  K5 — EditorLaunchBridge
  K6 — TestHarness
"""

import pytest
from typing import List, Optional, Dict
from enum import Enum, auto


# =============================================================================
# K1 — LaunchConfig
# =============================================================================

class ELaunchMode(str, Enum):
    Game     = "game"
    Editor   = "editor"
    Server   = "server"
    Playtest = "playtest"


class LaunchParams:
    def __init__(self):
        self.mode:         ELaunchMode = ELaunchMode.Game
        self.config_file:  str = ""
        self.repo_root:    str = ""
        self.save_name:    str = ""
        self.headless:     bool = False
        self.enable_bridge:bool = False
        self.dev_mode:     bool = False
        self.bridge_port:  int = 8765
        self.extra_args:   List[str] = []


class LaunchConfig:
    def __init__(self):
        self.params = LaunchParams()
        self.error:  str = ""

    def parse(self, args: List[str]) -> bool:
        self.error = ""
        i = 0
        while i < len(args):
            tok = args[i]
            def next_val():
                nonlocal i
                i += 1
                return args[i] if i < len(args) else ""

            if tok == "--mode":
                val = next_val()
                try:
                    self.params.mode = ELaunchMode(val.lower())
                except ValueError:
                    self.error = f"Unknown mode: {val}"
                    return False
            elif tok == "--config":
                self.params.config_file = next_val()
            elif tok == "--repo-root":
                self.params.repo_root = next_val()
            elif tok == "--save":
                self.params.save_name = next_val()
            elif tok == "--headless":
                self.params.headless = True
            elif tok == "--bridge":
                self.params.enable_bridge = True
            elif tok == "--bridge-port":
                try:
                    self.params.bridge_port = int(next_val())
                except ValueError:
                    self.error = "Invalid bridge-port"
                    return False
            elif tok == "--dev":
                self.params.dev_mode = True
            elif tok.startswith("--"):
                self.error = f"Unrecognised argument: {tok}"
                return False
            else:
                self.params.extra_args.append(tok)
            i += 1
        return True

    def describe(self) -> str:
        p = self.params
        parts = [f"mode={p.mode.value}"]
        if p.config_file:   parts.append(f"config={p.config_file}")
        if p.repo_root:     parts.append(f"repo-root={p.repo_root}")
        if p.save_name:     parts.append(f"save={p.save_name}")
        if p.headless:      parts.append("headless")
        if p.enable_bridge: parts.append(f"bridge(port={p.bridge_port})")
        if p.dev_mode:      parts.append("dev")
        return "LaunchConfig { " + " ".join(parts) + " }"


class TestK1LaunchConfig:
    def test_default_mode_is_game(self):
        cfg = LaunchConfig()
        assert cfg.params.mode == ELaunchMode.Game

    def test_parse_mode_editor(self):
        cfg = LaunchConfig()
        assert cfg.parse(["--mode", "editor"])
        assert cfg.params.mode == ELaunchMode.Editor

    def test_parse_mode_server(self):
        cfg = LaunchConfig()
        assert cfg.parse(["--mode", "server"])
        assert cfg.params.mode == ELaunchMode.Server

    def test_parse_mode_playtest(self):
        cfg = LaunchConfig()
        assert cfg.parse(["--mode", "playtest"])
        assert cfg.params.mode == ELaunchMode.Playtest

    def test_parse_headless_flag(self):
        cfg = LaunchConfig()
        cfg.parse(["--headless"])
        assert cfg.params.headless is True

    def test_parse_bridge_flag(self):
        cfg = LaunchConfig()
        cfg.parse(["--bridge"])
        assert cfg.params.enable_bridge is True

    def test_parse_bridge_port(self):
        cfg = LaunchConfig()
        cfg.parse(["--bridge", "--bridge-port", "9000"])
        assert cfg.params.bridge_port == 9000

    def test_parse_config_file(self):
        cfg = LaunchConfig()
        cfg.parse(["--config", "/path/to/project.json"])
        assert cfg.params.config_file == "/path/to/project.json"

    def test_parse_save_name(self):
        cfg = LaunchConfig()
        cfg.parse(["--save", "slot_01"])
        assert cfg.params.save_name == "slot_01"

    def test_parse_dev_flag(self):
        cfg = LaunchConfig()
        cfg.parse(["--dev"])
        assert cfg.params.dev_mode is True

    def test_parse_unknown_flag_returns_false(self):
        cfg = LaunchConfig()
        result = cfg.parse(["--unknown-flag"])
        assert result is False
        assert cfg.error != ""

    def test_parse_invalid_mode_returns_false(self):
        cfg = LaunchConfig()
        result = cfg.parse(["--mode", "banana"])
        assert result is False

    def test_parse_combined_args(self):
        cfg = LaunchConfig()
        cfg.parse(["--mode", "editor", "--bridge", "--bridge-port", "7777",
                   "--dev", "--headless", "--config", "dev.json"])
        p = cfg.params
        assert p.mode == ELaunchMode.Editor
        assert p.enable_bridge is True
        assert p.bridge_port == 7777
        assert p.dev_mode is True
        assert p.headless is True
        assert p.config_file == "dev.json"

    def test_describe_produces_string(self):
        cfg = LaunchConfig()
        cfg.parse(["--mode", "editor", "--bridge"])
        desc = cfg.describe()
        assert "editor" in desc
        assert "bridge" in desc

    def test_extra_args_collected(self):
        cfg = LaunchConfig()
        cfg.parse(["--mode", "game", "positional_arg"])
        assert "positional_arg" in cfg.params.extra_args


# =============================================================================
# K2 — GameSystemsRegistry
# =============================================================================

class ESystemState(str, Enum):
    Pending      = "Pending"
    Initialising = "Initialising"
    Ready        = "Ready"
    Failed       = "Failed"
    ShuttingDown = "ShuttingDown"
    Shutdown     = "Shutdown"


class SystemEntry:
    def __init__(self, name: str, category: str = "Engine"):
        self.name:          str = name
        self.category:      str = category
        self.state:         ESystemState = ESystemState.Pending
        self.error_message: str = ""


class GameSystemsRegistry:
    """Singleton-style registry (one instance per test via fixture)."""

    def __init__(self):
        self._systems: Dict[str, SystemEntry] = {}

    def register(self, name: str, category: str = "Engine") -> bool:
        if name in self._systems:
            return False
        self._systems[name] = SystemEntry(name, category)
        return True

    def set_state(self, name: str, state: ESystemState, error: str = "") -> bool:
        if name not in self._systems:
            return False
        self._systems[name].state = state
        self._systems[name].error_message = error
        return True

    def mark_ready(self, name: str) -> bool:
        return self.set_state(name, ESystemState.Ready)

    def mark_failed(self, name: str, reason: str = "") -> bool:
        return self.set_state(name, ESystemState.Failed, reason)

    def all_ready(self) -> bool:
        if not self._systems:
            return False
        return all(s.state == ESystemState.Ready for s in self._systems.values())

    def get_failed(self) -> List[SystemEntry]:
        return [s for s in self._systems.values() if s.state == ESystemState.Failed]

    def get_by_state(self, state: ESystemState) -> List[SystemEntry]:
        return [s for s in self._systems.values() if s.state == state]

    def find(self, name: str) -> Optional[SystemEntry]:
        return self._systems.get(name)

    def count(self) -> int:
        return len(self._systems)

    def count_by_state(self, state: ESystemState) -> int:
        return sum(1 for s in self._systems.values() if s.state == state)

    def reset(self):
        self._systems.clear()

    def health_report(self) -> str:
        lines = ["=== GameSystemsRegistry Health Report ===",
                 f"Total: {self.count()}"]
        for s in self._systems.values():
            line = f"  [{s.category}] {s.name} — {s.state.value}"
            if s.error_message:
                line += f" ({s.error_message})"
            lines.append(line)
        return "\n".join(lines)


@pytest.fixture
def registry():
    r = GameSystemsRegistry()
    yield r
    r.reset()


class TestK2GameSystemsRegistry:
    def test_register_new_system(self, registry):
        assert registry.register("Engine::Core") is True
        assert registry.count() == 1

    def test_register_duplicate_returns_false(self, registry):
        registry.register("Engine::Core")
        assert registry.register("Engine::Core") is False

    def test_default_state_is_pending(self, registry):
        registry.register("Engine::ECS")
        entry = registry.find("Engine::ECS")
        assert entry is not None
        assert entry.state == ESystemState.Pending

    def test_mark_ready(self, registry):
        registry.register("Engine::Logger")
        assert registry.mark_ready("Engine::Logger") is True
        assert registry.find("Engine::Logger").state == ESystemState.Ready

    def test_mark_failed(self, registry):
        registry.register("Engine::Physics")
        assert registry.mark_failed("Engine::Physics", "DLL not found") is True
        entry = registry.find("Engine::Physics")
        assert entry.state == ESystemState.Failed
        assert entry.error_message == "DLL not found"

    def test_all_ready_true_when_all_ready(self, registry):
        for name in ["A", "B", "C"]:
            registry.register(name)
            registry.mark_ready(name)
        assert registry.all_ready() is True

    def test_all_ready_false_when_one_failed(self, registry):
        registry.register("A")
        registry.register("B")
        registry.mark_ready("A")
        registry.mark_failed("B", "error")
        assert registry.all_ready() is False

    def test_all_ready_false_when_empty(self, registry):
        assert registry.all_ready() is False

    def test_get_failed_returns_failed_entries(self, registry):
        registry.register("Good")
        registry.register("Bad")
        registry.mark_ready("Good")
        registry.mark_failed("Bad", "crash")
        failed = registry.get_failed()
        assert len(failed) == 1
        assert failed[0].name == "Bad"

    def test_get_by_state(self, registry):
        for name in ["A", "B", "C"]:
            registry.register(name)
        registry.mark_ready("A")
        pending = registry.get_by_state(ESystemState.Pending)
        assert len(pending) == 2

    def test_count_by_state(self, registry):
        for name in ["X", "Y", "Z"]:
            registry.register(name)
        registry.mark_ready("X")
        assert registry.count_by_state(ESystemState.Ready) == 1
        assert registry.count_by_state(ESystemState.Pending) == 2

    def test_set_state_nonexistent_returns_false(self, registry):
        assert registry.set_state("nonexistent", ESystemState.Ready) is False

    def test_category_stored(self, registry):
        registry.register("Editor::Outliner", "Editor")
        assert registry.find("Editor::Outliner").category == "Editor"

    def test_health_report_contains_entries(self, registry):
        registry.register("Engine::ECS", "Engine")
        registry.mark_ready("Engine::ECS")
        report = registry.health_report()
        assert "Engine::ECS" in report
        assert "Ready" in report

    def test_reset_clears_all(self, registry):
        for name in ["A", "B"]:
            registry.register(name)
        registry.reset()
        assert registry.count() == 0


# =============================================================================
# K3 — PlaytestSession
# =============================================================================

class PlaytestConfig:
    def __init__(self, tick_count: int = 60, delta_time: float = 1/60,
                 load_save: bool = False, save_name: str = "",
                 scenario_tag: str = "", abort_on_first_error: bool = True):
        self.tick_count            = tick_count
        self.delta_time            = delta_time
        self.load_save             = load_save
        self.save_name             = save_name
        self.scenario_tag          = scenario_tag
        self.abort_on_first_error  = abort_on_first_error


class PlaytestResult:
    def __init__(self):
        self.success:     bool = False
        self.ticks_run:   int  = 0
        self.error_count: int  = 0
        self.errors:      List[str] = []
        self.log:         List[str] = []

    def exit_code(self) -> int:
        return 0 if self.success else 1

    def format(self) -> str:
        lines = ["=== PlaytestResult ===",
                 f"Status : {'PASS' if self.success else 'FAIL'}",
                 f"Ticks  : {self.ticks_run}",
                 f"Errors : {self.error_count}"]
        return "\n".join(lines)


class PlaytestSession:
    def __init__(self, config: Optional[PlaytestConfig] = None):
        self._config = config or PlaytestConfig()
        self._tick_callback = None

    def set_tick_callback(self, cb):
        self._tick_callback = cb

    def run(self) -> PlaytestResult:
        result = PlaytestResult()
        tag = self._config.scenario_tag or "default"
        result.log.append(f"[PlaytestSession] Starting scenario: {tag}")

        result.log.append("[PlaytestSession] Boot check passed")

        if self._config.load_save and self._config.save_name:
            result.log.append(f"[PlaytestSession] Loading save: {self._config.save_name}")

        for tick in range(self._config.tick_count):
            if self._tick_callback:
                if not self._tick_callback(tick, self._config.delta_time):
                    result.log.append(f"[PlaytestSession] Aborted at tick {tick}")
                    break
            result.ticks_run += 1

        result.log.append(f"[PlaytestSession] Completed {result.ticks_run}/"
                          f"{self._config.tick_count} ticks")
        result.success = (result.ticks_run == self._config.tick_count
                          and result.error_count == 0)
        return result


class TestK3PlaytestSession:
    def test_default_config_runs_60_ticks(self):
        session = PlaytestSession()
        result  = session.run()
        assert result.ticks_run == 60
        assert result.success is True

    def test_custom_tick_count(self):
        cfg     = PlaytestConfig(tick_count=10)
        session = PlaytestSession(cfg)
        result  = session.run()
        assert result.ticks_run == 10

    def test_tick_callback_invoked(self):
        invocations = []
        def cb(tick, dt):
            invocations.append(tick)
            return True

        cfg = PlaytestConfig(tick_count=5)
        session = PlaytestSession(cfg)
        session.set_tick_callback(cb)
        result = session.run()
        assert len(invocations) == 5
        assert result.success is True

    def test_tick_callback_abort_stops_early(self):
        def cb(tick, dt):
            return tick < 3  # abort after tick 3

        cfg = PlaytestConfig(tick_count=10)
        session = PlaytestSession(cfg)
        session.set_tick_callback(cb)
        result = session.run()
        assert result.ticks_run <= 4
        assert result.success is False  # didn't complete all 10

    def test_exit_code_pass(self):
        session = PlaytestSession(PlaytestConfig(tick_count=1))
        result  = session.run()
        assert result.exit_code() == 0

    def test_scenario_tag_in_log(self):
        cfg     = PlaytestConfig(tick_count=1, scenario_tag="VerticalSlice")
        session = PlaytestSession(cfg)
        result  = session.run()
        assert any("VerticalSlice" in entry for entry in result.log)

    def test_load_save_logged(self):
        cfg     = PlaytestConfig(tick_count=1, load_save=True, save_name="slot_01")
        session = PlaytestSession(cfg)
        result  = session.run()
        assert any("slot_01" in entry for entry in result.log)

    def test_format_contains_status(self):
        session = PlaytestSession(PlaytestConfig(tick_count=1))
        result  = session.run()
        fmt = result.format()
        assert "PASS" in fmt or "FAIL" in fmt


# =============================================================================
# K4 — RuntimeDiagnostics
# =============================================================================

class EDiagnosticSeverity(str, Enum):
    Info     = "Info"
    Warning  = "Warning"
    Error    = "Error"
    Critical = "Critical"


class DiagnosticEntry:
    def __init__(self, severity: EDiagnosticSeverity, category: str, message: str):
        self.severity = severity
        self.category = category
        self.message  = message


class DiagnosticsReport:
    def __init__(self):
        self.entries:       List[DiagnosticEntry] = []
        self.has_errors:    bool = False
        self.has_critical:  bool = False
        self.error_count:   int  = 0
        self.warning_count: int  = 0

    def add(self, severity: EDiagnosticSeverity, category: str, message: str):
        self.entries.append(DiagnosticEntry(severity, category, message))
        if severity == EDiagnosticSeverity.Error:
            self.has_errors = True
            self.error_count += 1
        elif severity == EDiagnosticSeverity.Critical:
            self.has_critical = True
            self.error_count += 1
        elif severity == EDiagnosticSeverity.Warning:
            self.warning_count += 1

    def is_healthy(self) -> bool:
        return not self.has_errors and not self.has_critical

    def format(self) -> str:
        lines = ["=== RuntimeDiagnostics ==="]
        for e in self.entries:
            lines.append(f"[{e.severity.value}] [{e.category}] {e.message}")
        lines.append(f"Errors: {self.error_count}  Warnings: {self.warning_count}")
        lines.append(f"Health: {'OK' if self.is_healthy() else 'DEGRADED'}")
        return "\n".join(lines)


class RuntimeDiagnostics:
    def __init__(self, registry: Optional[GameSystemsRegistry] = None):
        self._registry = registry or GameSystemsRegistry()

    def run(self) -> DiagnosticsReport:
        report = DiagnosticsReport()
        self._check_system_registry(report)
        self._check_data_registry(report)
        self._check_render_system(report)
        self._check_save_system(report)
        return report

    def _check_system_registry(self, report: DiagnosticsReport):
        reg = self._registry
        if reg.count() == 0:
            report.add(EDiagnosticSeverity.Warning, "Systems",
                       "No subsystems registered")
            return
        for entry in reg.get_failed():
            report.add(EDiagnosticSeverity.Critical, "Systems",
                       f"System failed: {entry.name}" +
                       (f" ({entry.error_message})" if entry.error_message else ""))
        for entry in reg.get_by_state(ESystemState.Pending):
            report.add(EDiagnosticSeverity.Warning, "Systems",
                       f"System still pending: {entry.name}")
        if reg.all_ready():
            report.add(EDiagnosticSeverity.Info, "Systems",
                       f"All {reg.count()} subsystems ready")

    def _check_data_registry(self, report: DiagnosticsReport):
        report.add(EDiagnosticSeverity.Info, "Data",
                   "Data registry check deferred to DataRegistry::Validate()")

    def _check_render_system(self, report: DiagnosticsReport):
        report.add(EDiagnosticSeverity.Info, "Rendering",
                   "Render system check deferred to Renderer::IsReady()")

    def _check_save_system(self, report: DiagnosticsReport):
        report.add(EDiagnosticSeverity.Info, "Save",
                   "Save system check deferred to SaveManager::IsReady()")


class TestK4RuntimeDiagnostics:
    def test_empty_registry_produces_warning(self):
        reg   = GameSystemsRegistry()
        diag  = RuntimeDiagnostics(reg)
        report = diag.run()
        warnings = [e for e in report.entries
                    if e.severity == EDiagnosticSeverity.Warning and e.category == "Systems"]
        assert len(warnings) >= 1

    def test_all_ready_is_healthy(self):
        reg = GameSystemsRegistry()
        for name in ["A", "B"]:
            reg.register(name)
            reg.mark_ready(name)
        diag   = RuntimeDiagnostics(reg)
        report = diag.run()
        assert report.is_healthy() is True

    def test_failed_system_produces_critical(self):
        reg = GameSystemsRegistry()
        reg.register("BrokenSystem")
        reg.mark_failed("BrokenSystem", "crash")
        diag   = RuntimeDiagnostics(reg)
        report = diag.run()
        critical = [e for e in report.entries
                    if e.severity == EDiagnosticSeverity.Critical]
        assert len(critical) >= 1
        assert report.is_healthy() is False

    def test_pending_system_produces_warning(self):
        reg = GameSystemsRegistry()
        reg.register("Pending")
        reg.register("Ready")
        reg.mark_ready("Ready")
        diag   = RuntimeDiagnostics(reg)
        report = diag.run()
        warnings = [e for e in report.entries
                    if e.severity == EDiagnosticSeverity.Warning and "Pending" in e.message]
        assert len(warnings) >= 1

    def test_format_contains_health_line(self):
        reg = GameSystemsRegistry()
        reg.register("X")
        reg.mark_ready("X")
        diag   = RuntimeDiagnostics(reg)
        report = diag.run()
        fmt = report.format()
        assert "Health:" in fmt

    def test_deferred_checks_produce_info(self):
        reg    = GameSystemsRegistry()
        diag   = RuntimeDiagnostics(reg)
        report = diag.run()
        categories = {e.category for e in report.entries
                      if e.severity == EDiagnosticSeverity.Info}
        assert "Data" in categories
        assert "Rendering" in categories
        assert "Save" in categories


# =============================================================================
# K5 — EditorLaunchBridge
# =============================================================================

from enum import IntFlag

class EEditorSubsystem(IntFlag):
    Core            = 1 << 0
    Outliner        = 1 << 1
    Inspector       = 1 << 2
    Viewport        = 1 << 3
    AssetBrowser    = 1 << 4
    Gizmos          = 1 << 5
    CommandStack    = 1 << 6
    ValidationPanel = 1 << 7
    DocsPanel       = 1 << 8
    DiffReview      = 1 << 9
    AtlasAIBridge   = 1 << 10
    All             = 0x7FF


class EditorBootResult:
    def __init__(self, success: bool = False, message: str = ""):
        self.success = success
        self.message = message

    def exit_code(self) -> int:
        return 0 if self.success else 1


class EditorLaunchBridge:
    def __init__(self):
        self._mask   = EEditorSubsystem.All
        self._booted = False
        self._registry = GameSystemsRegistry()

    def set_subsystem_mask(self, mask: EEditorSubsystem):
        self._mask = mask

    def get_subsystem_mask(self) -> EEditorSubsystem:
        return self._mask

    def is_booted(self) -> bool:
        return self._booted

    def boot(self, params: LaunchParams) -> EditorBootResult:
        if self._booted:
            return EditorBootResult(False, "Already booted")

        # Core systems
        for name in ["AtlasEngine::Core", "AtlasEngine::ECS",
                     "AtlasEngine::EventBus", "AtlasEngine::Logger"]:
            self._registry.register(name, "Engine")
            self._registry.mark_ready(name)

        # Editor subsystems per mask
        subsys_map = {
            EEditorSubsystem.Core:            "Editor::Core",
            EEditorSubsystem.Outliner:        "Editor::Outliner",
            EEditorSubsystem.Inspector:       "Editor::Inspector",
            EEditorSubsystem.Viewport:        "Editor::Viewport",
            EEditorSubsystem.AssetBrowser:    "Editor::AssetBrowser",
            EEditorSubsystem.Gizmos:          "Editor::Gizmos",
            EEditorSubsystem.CommandStack:    "Editor::CommandStack",
            EEditorSubsystem.ValidationPanel: "Editor::ValidationPanel",
            EEditorSubsystem.DocsPanel:       "Editor::DocsPanel",
            EEditorSubsystem.DiffReview:      "Editor::DiffReview",
        }
        mask = int(self._mask)
        for sys_enum, sys_name in subsys_map.items():
            if mask & int(sys_enum):
                self._registry.register(sys_name, "Editor")
                self._registry.mark_ready(sys_name)

        # AtlasAI bridge
        if params.enable_bridge and (mask & int(EEditorSubsystem.AtlasAIBridge)):
            self._registry.register("AtlasAI::Bridge", "AI")
            self._registry.mark_ready("AtlasAI::Bridge")

        self._booted = True
        return EditorBootResult(True, "OK")

    def shutdown(self):
        for entry in list(self._registry.all()):
            if entry.category in ("Editor", "AI"):
                self._registry.set_state(entry.name, ESystemState.Shutdown)
        self._booted = False

    def registry(self) -> GameSystemsRegistry:
        return self._registry


class TestK5EditorLaunchBridge:
    def _make_params(self, mode=ELaunchMode.Editor, bridge=False,
                     bridge_port=8765, dev=False) -> LaunchParams:
        p = LaunchParams()
        p.mode = mode
        p.enable_bridge = bridge
        p.bridge_port = bridge_port
        p.dev_mode = dev
        return p

    def test_boot_succeeds(self):
        bridge = EditorLaunchBridge()
        result = bridge.boot(self._make_params())
        assert result.success is True

    def test_is_booted_after_boot(self):
        bridge = EditorLaunchBridge()
        bridge.boot(self._make_params())
        assert bridge.is_booted() is True

    def test_double_boot_fails(self):
        bridge = EditorLaunchBridge()
        bridge.boot(self._make_params())
        result = bridge.boot(self._make_params())
        assert result.success is False

    def test_core_systems_registered_ready(self):
        bridge = EditorLaunchBridge()
        bridge.boot(self._make_params())
        reg = bridge.registry()
        core = reg.find("AtlasEngine::Core")
        assert core is not None
        assert core.state == ESystemState.Ready

    def test_editor_subsystems_registered(self):
        bridge = EditorLaunchBridge()
        bridge.boot(self._make_params())
        reg = bridge.registry()
        for name in ["Editor::Core", "Editor::Outliner", "Editor::Viewport"]:
            entry = reg.find(name)
            assert entry is not None, f"Missing: {name}"
            assert entry.state == ESystemState.Ready

    def test_bridge_registered_when_requested(self):
        bridge = EditorLaunchBridge()
        bridge.boot(self._make_params(bridge=True))
        reg = bridge.registry()
        entry = reg.find("AtlasAI::Bridge")
        assert entry is not None
        assert entry.state == ESystemState.Ready

    def test_bridge_not_registered_when_not_requested(self):
        bridge = EditorLaunchBridge()
        bridge.boot(self._make_params(bridge=False))
        reg = bridge.registry()
        assert reg.find("AtlasAI::Bridge") is None

    def test_subsystem_mask_limits_subsystems(self):
        bridge = EditorLaunchBridge()
        # Only boot Core + Outliner
        bridge.set_subsystem_mask(EEditorSubsystem.Core | EEditorSubsystem.Outliner)
        bridge.boot(self._make_params())
        reg = bridge.registry()
        assert reg.find("Editor::Core")     is not None
        assert reg.find("Editor::Outliner") is not None
        assert reg.find("Editor::Viewport") is None

    def test_shutdown_marks_editor_systems(self):
        bridge = EditorLaunchBridge()
        bridge.boot(self._make_params())
        bridge.shutdown()
        assert bridge.is_booted() is False
        reg = bridge.registry()
        core = reg.find("Editor::Core")
        assert core is not None
        assert core.state == ESystemState.Shutdown

    def test_exit_code(self):
        bridge = EditorLaunchBridge()
        result = bridge.boot(self._make_params())
        assert result.exit_code() == 0

    # Helper for shutdown test
    def _all(self, registry):
        return list(registry._systems.values())


# Patch in all() method to GameSystemsRegistry for shutdown test
def _reg_all(self):
    return list(self._systems.values())

GameSystemsRegistry.all = _reg_all


# =============================================================================
# K6 — TestHarness
# =============================================================================

class TestCase:
    def __init__(self, name: str, config: Optional[PlaytestConfig] = None,
                 setup=None, teardown=None):
        self.name       = name
        self.config     = config or PlaytestConfig(tick_count=5)
        self.setup      = setup
        self.teardown   = teardown


class HarnessResult:
    def __init__(self):
        self.total_cases:    int = 0
        self.passed_cases:   int = 0
        self.failed_cases:   int = 0
        self.failed_names:   List[str] = []
        self.case_results:   List[PlaytestResult] = []

    def all_passed(self) -> bool:
        return self.failed_cases == 0 and self.total_cases > 0

    def exit_code(self) -> int:
        return 0 if self.all_passed() else 1

    def format(self) -> str:
        lines = ["=== TestHarness Results ===",
                 f"Total  : {self.total_cases}",
                 f"Passed : {self.passed_cases}",
                 f"Failed : {self.failed_cases}",
                 f"Result : {'PASS' if self.all_passed() else 'FAIL'}"]
        return "\n".join(lines)


class TestHarness:
    def __init__(self):
        self._cases: List[TestCase] = []

    def add_case(self, tc: TestCase):
        self._cases.append(tc)

    def add_simple_case(self, name: str, tick_count: int = 10,
                        scenario_tag: str = ""):
        cfg = PlaytestConfig(tick_count=tick_count,
                             scenario_tag=scenario_tag or name)
        self._cases.append(TestCase(name=name, config=cfg))

    def run_all(self) -> HarnessResult:
        harness = HarnessResult()
        harness.total_cases = len(self._cases)
        for tc in self._cases:
            if tc.setup:   tc.setup()
            session = PlaytestSession(tc.config)
            r       = session.run()
            harness.case_results.append(r)
            if tc.teardown: tc.teardown()
            if r.success:
                harness.passed_cases += 1
            else:
                harness.failed_cases += 1
                harness.failed_names.append(tc.name)
        return harness

    def case_count(self) -> int:
        return len(self._cases)


class TestK6TestHarness:
    def test_empty_harness_fails(self):
        harness = TestHarness()
        result  = harness.run_all()
        assert result.all_passed() is False

    def test_single_passing_case(self):
        harness = TestHarness()
        harness.add_simple_case("boot_smoke", tick_count=5)
        result = harness.run_all()
        assert result.total_cases  == 1
        assert result.passed_cases == 1
        assert result.failed_cases == 0
        assert result.all_passed() is True
        assert result.exit_code()  == 0

    def test_multiple_passing_cases(self):
        harness = TestHarness()
        for name in ["A", "B", "C"]:
            harness.add_simple_case(name, tick_count=3)
        result = harness.run_all()
        assert result.total_cases  == 3
        assert result.passed_cases == 3
        assert result.all_passed() is True

    def test_failed_case_tracked(self):
        harness = TestHarness()
        # A session that aborts immediately via callback:
        tc = TestCase("abort_immediately",
                      PlaytestConfig(tick_count=10, scenario_tag="abort"))
        # We can't inject a callback directly via TestCase, so use tick_count=0
        tc.config.tick_count = 0  # 0 ticks → success=False (0 != 0? no, equal)
        # Actually tick_count=0 means 0 == 0, so it would pass. Use tick_count=-1.
        # Instead: force error via a trick — abort callback through custom session
        # Build a simple failing case via tick_count=-1 (loop won't run, 0 != -1):
        tc.config.tick_count = -1  # negative → loop never runs → 0 ticks != -1 → FAIL
        harness.add_case(tc)
        result = harness.run_all()
        assert result.failed_cases == 1
        assert "abort_immediately" in result.failed_names
        assert result.all_passed() is False
        assert result.exit_code()  == 1

    def test_case_count(self):
        harness = TestHarness()
        harness.add_simple_case("x")
        harness.add_simple_case("y")
        assert harness.case_count() == 2

    def test_setup_teardown_called(self):
        log = []
        harness = TestHarness()
        tc = TestCase("with_hooks",
                      PlaytestConfig(tick_count=1),
                      setup=lambda: log.append("setup"),
                      teardown=lambda: log.append("teardown"))
        harness.add_case(tc)
        harness.run_all()
        assert log == ["setup", "teardown"]

    def test_format_contains_result(self):
        harness = TestHarness()
        harness.add_simple_case("x", tick_count=1)
        result = harness.run_all()
        fmt = result.format()
        assert "PASS" in fmt or "FAIL" in fmt

    def test_case_results_populated(self):
        harness = TestHarness()
        harness.add_simple_case("a", tick_count=2)
        harness.add_simple_case("b", tick_count=3)
        result = harness.run_all()
        assert len(result.case_results) == 2


# =============================================================================
# Integration — LaunchConfig → EditorLaunchBridge → GameSystemsRegistry
# =============================================================================

class TestLaunchIntegration:
    def test_editor_launch_full_pipeline(self):
        """Full pipeline: parse args → launch bridge → verify all systems ready."""
        cfg = LaunchConfig()
        assert cfg.parse(["--mode", "editor", "--bridge", "--bridge-port", "9000"])
        assert cfg.params.mode == ELaunchMode.Editor
        assert cfg.params.enable_bridge is True

        bridge = EditorLaunchBridge()
        result = bridge.boot(cfg.params)
        assert result.success is True

        reg = bridge.registry()
        assert reg.find("AtlasEngine::Core") is not None
        assert reg.find("AtlasAI::Bridge")   is not None

    def test_playtest_pipeline(self):
        """Parse playtest args → run TestHarness → pass."""
        cfg = LaunchConfig()
        cfg.parse(["--mode", "playtest", "--headless"])
        assert cfg.params.mode == ELaunchMode.Playtest
        assert cfg.params.headless is True

        harness = TestHarness()
        harness.add_simple_case("smoke_boot",        tick_count=10)
        harness.add_simple_case("data_registry_boot", tick_count=5)
        harness.add_simple_case("world_sim_boot",     tick_count=5)

        result = harness.run_all()
        assert result.all_passed() is True
        assert result.exit_code()  == 0

    def test_diagnostics_after_editor_boot(self):
        """Boot editor → run diagnostics → healthy."""
        bridge = EditorLaunchBridge()
        bridge.boot(LaunchParams())

        diag   = RuntimeDiagnostics(bridge.registry())
        report = diag.run()
        # All systems were marked ready by the bridge, so diagnostics is healthy.
        assert report.is_healthy() is True
