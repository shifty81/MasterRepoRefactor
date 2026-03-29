"""Phase 35B — Tests for MatchmakingPipeline and ConversationGraphPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    MatchmakingPipeline,
    MatchmakingRuleSet,
    MatchSession,
    MatchResult,
    ConversationGraphPipeline,
    ConversationNodeDef,
    ConversationEdgeDef,
    ConversationGraphEntry,
)


# ---------------------------------------------------------------------------
# MatchmakingRuleSet
# ---------------------------------------------------------------------------

class TestMatchmakingRuleSet(unittest.TestCase):
    def test_ruleset_id(self):
        r = MatchmakingRuleSet(ruleset_id="rs_001", ruleset_name="Default Rules")
        self.assertEqual(r.ruleset_id, "rs_001")

    def test_ruleset_name(self):
        r = MatchmakingRuleSet(ruleset_id="rs_001", ruleset_name="Default Rules")
        self.assertEqual(r.ruleset_name, "Default Rules")

    def test_default_min_players(self):
        r = MatchmakingRuleSet(ruleset_id="rs_001", ruleset_name="Default Rules")
        self.assertEqual(r.min_players, 2)

    def test_default_max_players(self):
        r = MatchmakingRuleSet(ruleset_id="rs_001", ruleset_name="Default Rules")
        self.assertEqual(r.max_players, 16)

    def test_is_strict_region_false(self):
        r = MatchmakingRuleSet(ruleset_id="rs_001", ruleset_name="Default Rules")
        self.assertFalse(r.is_strict_region)

    def test_has_skill_matching_true(self):
        r = MatchmakingRuleSet(ruleset_id="rs_001", ruleset_name="Default Rules", skill_tolerance=100.0)
        self.assertTrue(r.has_skill_matching)


# ---------------------------------------------------------------------------
# MatchSession
# ---------------------------------------------------------------------------

class TestMatchSession(unittest.TestCase):
    def test_session_id(self):
        s = MatchSession(session_id="sess_001", session_name="Game Session 1")
        self.assertEqual(s.session_id, "sess_001")

    def test_session_name(self):
        s = MatchSession(session_id="sess_001", session_name="Game Session 1")
        self.assertEqual(s.session_name, "Game Session 1")

    def test_default_state(self):
        s = MatchSession(session_id="sess_001", session_name="Game Session 1")
        self.assertEqual(s.session_state, "Pending")

    def test_is_full_false(self):
        s = MatchSession(session_id="sess_001", session_name="Game Session 1")
        self.assertFalse(s.is_full)

    def test_is_active_false(self):
        s = MatchSession(session_id="sess_001", session_name="Game Session 1")
        self.assertFalse(s.is_active)

    def test_has_ruleset_false(self):
        s = MatchSession(session_id="sess_001", session_name="Game Session 1")
        self.assertFalse(s.has_ruleset)


# ---------------------------------------------------------------------------
# MatchResult
# ---------------------------------------------------------------------------

class TestMatchResult(unittest.TestCase):
    def test_result_id(self):
        r = MatchResult(result_id="res_001", session_id="sess_001")
        self.assertEqual(r.result_id, "res_001")

    def test_session_id(self):
        r = MatchResult(result_id="res_001", session_id="sess_001")
        self.assertEqual(r.session_id, "sess_001")

    def test_default_outcome(self):
        r = MatchResult(result_id="res_001", session_id="sess_001")
        self.assertEqual(r.outcome, "Undecided")

    def test_is_decided_false(self):
        r = MatchResult(result_id="res_001", session_id="sess_001")
        self.assertFalse(r.is_decided)

    def test_has_scores_false(self):
        r = MatchResult(result_id="res_001", session_id="sess_001")
        self.assertFalse(r.has_scores)


# ---------------------------------------------------------------------------
# MatchmakingPipeline
# ---------------------------------------------------------------------------

class TestMatchmakingPipeline(unittest.TestCase):
    def _pipeline(self):
        return MatchmakingPipeline()

    def _ruleset(self, rid="rs_001"):
        return MatchmakingRuleSet(ruleset_id=rid, ruleset_name="Default Rules")

    def _session(self, sid="sess_001"):
        return MatchSession(session_id=sid, session_name="Game Session 1")

    def test_add_ruleset(self):
        pipe = self._pipeline()
        pipe.add_ruleset(self._ruleset())
        self.assertIsNotNone(pipe.get_ruleset("rs_001"))

    def test_remove_ruleset(self):
        pipe = self._pipeline()
        pipe.add_ruleset(self._ruleset())
        self.assertTrue(pipe.remove_ruleset("rs_001"))
        self.assertIsNone(pipe.get_ruleset("rs_001"))

    def test_get_all_rulesets(self):
        pipe = self._pipeline()
        pipe.add_ruleset(self._ruleset("rs_001"))
        pipe.add_ruleset(self._ruleset("rs_002"))
        self.assertEqual(len(pipe.get_all_rulesets()), 2)

    def test_create_session(self):
        pipe = self._pipeline()
        pipe.create_session(self._session())
        self.assertEqual(pipe.session_count, 1)

    def test_close_session(self):
        pipe = self._pipeline()
        pipe.create_session(self._session())
        self.assertTrue(pipe.close_session("sess_001"))
        self.assertEqual(pipe.session_count, 0)

    def test_get_session(self):
        pipe = self._pipeline()
        pipe.create_session(self._session())
        self.assertIsNotNone(pipe.get_session("sess_001"))

    def test_get_all_sessions(self):
        pipe = self._pipeline()
        pipe.create_session(self._session("sess_001"))
        pipe.create_session(self._session("sess_002"))
        self.assertEqual(len(pipe.get_all_sessions()), 2)

    def test_add_player(self):
        pipe = self._pipeline()
        pipe.create_session(self._session())
        self.assertTrue(pipe.add_player("sess_001", "player_001"))
        session = pipe.get_session("sess_001")
        self.assertIn("player_001", session.players)

    def test_remove_player(self):
        pipe = self._pipeline()
        pipe.create_session(self._session())
        pipe.add_player("sess_001", "player_001")
        self.assertTrue(pipe.remove_player("sess_001", "player_001"))

    def test_set_session_state(self):
        pipe = self._pipeline()
        pipe.create_session(self._session())
        self.assertTrue(pipe.set_session_state("sess_001", "Active"))
        session = pipe.get_session("sess_001")
        self.assertEqual(session.session_state, "Active")

    def test_record_result(self):
        pipe = self._pipeline()
        result = MatchResult(result_id="res_001", session_id="sess_001")
        pipe.record_result(result)
        self.assertIsNotNone(pipe.get_result("res_001"))

    def test_get_results_by_session(self):
        pipe = self._pipeline()
        pipe.record_result(MatchResult(result_id="res_001", session_id="sess_001"))
        pipe.record_result(MatchResult(result_id="res_002", session_id="sess_001"))
        results = pipe.get_results_by_session("sess_001")
        self.assertEqual(len(results), 2)

    def test_validate(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.validate(self._session()))

    def test_session_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.session_count, 0)
        pipe.create_session(self._session())
        self.assertEqual(pipe.session_count, 1)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.create_session(self._session())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


# ---------------------------------------------------------------------------
# ConversationNodeDef
# ---------------------------------------------------------------------------

class TestConversationNodeDef(unittest.TestCase):
    def test_node_id(self):
        n = ConversationNodeDef(node_id="node_001", node_name="Greeting")
        self.assertEqual(n.node_id, "node_001")

    def test_node_name(self):
        n = ConversationNodeDef(node_id="node_001", node_name="Greeting")
        self.assertEqual(n.node_name, "Greeting")

    def test_default_node_type(self):
        n = ConversationNodeDef(node_id="node_001", node_name="Greeting")
        self.assertEqual(n.node_type, "Dialogue")

    def test_is_dialogue_true(self):
        n = ConversationNodeDef(node_id="node_001", node_name="Greeting", node_type="Dialogue")
        self.assertTrue(n.is_dialogue)

    def test_has_conditions_false(self):
        n = ConversationNodeDef(node_id="node_001", node_name="Greeting")
        self.assertFalse(n.has_conditions)

    def test_has_actions_false(self):
        n = ConversationNodeDef(node_id="node_001", node_name="Greeting")
        self.assertFalse(n.has_actions)


# ---------------------------------------------------------------------------
# ConversationEdgeDef
# ---------------------------------------------------------------------------

class TestConversationEdgeDef(unittest.TestCase):
    def test_edge_id(self):
        e = ConversationEdgeDef(edge_id="edge_001", from_node_id="node_001", to_node_id="node_002")
        self.assertEqual(e.edge_id, "edge_001")

    def test_from_node_id(self):
        e = ConversationEdgeDef(edge_id="edge_001", from_node_id="node_001", to_node_id="node_002")
        self.assertEqual(e.from_node_id, "node_001")

    def test_to_node_id(self):
        e = ConversationEdgeDef(edge_id="edge_001", from_node_id="node_001", to_node_id="node_002")
        self.assertEqual(e.to_node_id, "node_002")

    def test_has_condition_false(self):
        e = ConversationEdgeDef(edge_id="edge_001", from_node_id="node_001", to_node_id="node_002")
        self.assertFalse(e.has_condition)

    def test_has_condition_true(self):
        e = ConversationEdgeDef(edge_id="edge_001", from_node_id="node_001", to_node_id="node_002", condition="quest_done")
        self.assertTrue(e.has_condition)


# ---------------------------------------------------------------------------
# ConversationGraphEntry
# ---------------------------------------------------------------------------

class TestConversationGraphEntry(unittest.TestCase):
    def test_graph_id(self):
        g = ConversationGraphEntry(graph_id="graph_001", graph_name="NPC Intro")
        self.assertEqual(g.graph_id, "graph_001")

    def test_graph_name(self):
        g = ConversationGraphEntry(graph_id="graph_001", graph_name="NPC Intro")
        self.assertEqual(g.graph_name, "NPC Intro")

    def test_is_empty_true(self):
        g = ConversationGraphEntry(graph_id="graph_001", graph_name="NPC Intro")
        self.assertTrue(g.is_empty)

    def test_has_entry_false(self):
        g = ConversationGraphEntry(graph_id="graph_001", graph_name="NPC Intro")
        self.assertFalse(g.has_entry)

    def test_has_edges_false(self):
        g = ConversationGraphEntry(graph_id="graph_001", graph_name="NPC Intro")
        self.assertFalse(g.has_edges)


# ---------------------------------------------------------------------------
# ConversationGraphPipeline
# ---------------------------------------------------------------------------

class TestConversationGraphPipeline(unittest.TestCase):
    def _pipeline(self):
        return ConversationGraphPipeline()

    def _graph(self, gid="graph_001"):
        return ConversationGraphEntry(graph_id=gid, graph_name="NPC Intro")

    def _node(self, nid="node_001"):
        return ConversationNodeDef(node_id=nid, node_name="Greeting")

    def _edge(self, eid="edge_001"):
        return ConversationEdgeDef(edge_id=eid, from_node_id="node_001", to_node_id="node_002")

    def test_add_graph(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        self.assertEqual(pipe.graph_count, 1)

    def test_remove_graph(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        self.assertTrue(pipe.remove_graph("graph_001"))
        self.assertEqual(pipe.graph_count, 0)

    def test_get_graph(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        self.assertIsNotNone(pipe.get_graph("graph_001"))

    def test_get_all_graphs(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph("graph_001"))
        pipe.add_graph(self._graph("graph_002"))
        self.assertEqual(len(pipe.get_all_graphs()), 2)

    def test_add_node(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        self.assertTrue(pipe.add_node("graph_001", self._node()))

    def test_remove_node(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        pipe.add_node("graph_001", self._node())
        self.assertTrue(pipe.remove_node("graph_001", "node_001"))

    def test_add_edge(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        self.assertTrue(pipe.add_edge("graph_001", self._edge()))

    def test_remove_edge(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        pipe.add_edge("graph_001", self._edge())
        self.assertTrue(pipe.remove_edge("graph_001", "edge_001"))

    def test_set_entry_node(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        pipe.add_node("graph_001", self._node())
        self.assertTrue(pipe.set_entry_node("graph_001", "node_001"))
        graph = pipe.get_graph("graph_001")
        self.assertEqual(graph.entry_node_id, "node_001")

    def test_get_nodes_by_type(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        pipe.add_node("graph_001", ConversationNodeDef(node_id="node_001", node_name="A", node_type="Dialogue"))
        pipe.add_node("graph_001", ConversationNodeDef(node_id="node_002", node_name="B", node_type="Choice"))
        result = pipe.get_nodes_by_type("graph_001", "Dialogue")
        self.assertEqual(len(result), 1)

    def test_get_edges_for_node(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        pipe.add_edge("graph_001", ConversationEdgeDef(edge_id="edge_001", from_node_id="node_001", to_node_id="node_002"))
        edges = pipe.get_edges_for_node("graph_001", "node_001")
        self.assertEqual(len(edges), 1)

    def test_validate(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.validate(self._graph()))

    def test_graph_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.graph_count, 0)
        pipe.add_graph(self._graph())
        self.assertEqual(pipe.graph_count, 1)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_graph(self._graph())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


if __name__ == "__main__":
    unittest.main()
