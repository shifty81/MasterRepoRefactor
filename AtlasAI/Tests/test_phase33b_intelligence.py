"""Phase 33B — Tests for GameplayAbilityPipeline and EnvironmentQueryPipeline."""
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "AtlasAI" / "AIEngine"))

from AtlasAIEngine.intelligence import (
    GameplayAbilityPipeline,
    AbilityEntry,
    AbilityCostDef,
    AbilityEffectDef,
    EnvironmentQueryPipeline,
    EQSGeneratorConfig,
    EQSTestConfig,
    EQSQueryResult,
)


# ---------------------------------------------------------------------------
# AbilityCostDef
# ---------------------------------------------------------------------------

class TestAbilityCostDef(unittest.TestCase):
    def test_cost_id(self):
        c = AbilityCostDef(cost_id="c001", cost_name="Mana Cost")
        self.assertEqual(c.cost_id, "c001")

    def test_cost_name(self):
        c = AbilityCostDef(cost_id="c001", cost_name="Mana Cost")
        self.assertEqual(c.cost_name, "Mana Cost")

    def test_default_attribute_name(self):
        c = AbilityCostDef(cost_id="c001", cost_name="Mana Cost")
        self.assertEqual(c.attribute_name, "Mana")

    def test_default_cost_value(self):
        c = AbilityCostDef(cost_id="c001", cost_name="Mana Cost")
        self.assertAlmostEqual(c.cost_value, 10.0)

    def test_is_enabled_true(self):
        c = AbilityCostDef(cost_id="c001", cost_name="Mana Cost")
        self.assertTrue(c.is_enabled)

    def test_has_attribute_true(self):
        c = AbilityCostDef(cost_id="c001", cost_name="Mana Cost", attribute_name="Mana")
        self.assertTrue(c.has_attribute)


# ---------------------------------------------------------------------------
# AbilityEffectDef
# ---------------------------------------------------------------------------

class TestAbilityEffectDef(unittest.TestCase):
    def test_effect_id(self):
        e = AbilityEffectDef(effect_id="e001", effect_name="Fireball Hit")
        self.assertEqual(e.effect_id, "e001")

    def test_effect_name(self):
        e = AbilityEffectDef(effect_id="e001", effect_name="Fireball Hit")
        self.assertEqual(e.effect_name, "Fireball Hit")

    def test_default_application_type(self):
        e = AbilityEffectDef(effect_id="e001", effect_name="Fireball Hit")
        self.assertEqual(e.application_type, "Instant")

    def test_default_duration(self):
        e = AbilityEffectDef(effect_id="e001", effect_name="Fireball Hit")
        self.assertAlmostEqual(e.duration, 0.0)

    def test_is_instant_true(self):
        e = AbilityEffectDef(effect_id="e001", effect_name="Fireball Hit", application_type="Instant")
        self.assertTrue(e.is_instant)

    def test_is_periodic_false(self):
        e = AbilityEffectDef(effect_id="e001", effect_name="Fireball Hit", application_type="Instant")
        self.assertFalse(e.is_periodic)


# ---------------------------------------------------------------------------
# AbilityEntry
# ---------------------------------------------------------------------------

class TestAbilityEntry(unittest.TestCase):
    def test_entry_id(self):
        a = AbilityEntry(entry_id="a001", ability_name="Fireball")
        self.assertEqual(a.entry_id, "a001")

    def test_ability_name(self):
        a = AbilityEntry(entry_id="a001", ability_name="Fireball")
        self.assertEqual(a.ability_name, "Fireball")

    def test_default_activation_policy(self):
        a = AbilityEntry(entry_id="a001", ability_name="Fireball")
        self.assertEqual(a.activation_policy, "OnInputAction")

    def test_default_end_policy(self):
        a = AbilityEntry(entry_id="a001", ability_name="Fireball")
        self.assertEqual(a.end_policy, "WhenCompleted")

    def test_is_compiled_false(self):
        a = AbilityEntry(entry_id="a001", ability_name="Fireball")
        self.assertFalse(a.is_compiled)

    def test_has_costs_false(self):
        a = AbilityEntry(entry_id="a001", ability_name="Fireball")
        self.assertFalse(a.has_costs)

    def test_has_effects_false(self):
        a = AbilityEntry(entry_id="a001", ability_name="Fireball")
        self.assertFalse(a.has_effects)


# ---------------------------------------------------------------------------
# GameplayAbilityPipeline
# ---------------------------------------------------------------------------

class TestGameplayAbilityPipeline(unittest.TestCase):
    def _pipeline(self):
        return GameplayAbilityPipeline()

    def _entry(self, eid="a001"):
        return AbilityEntry(entry_id=eid, ability_name="Fireball")

    def test_add_ability(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        self.assertEqual(pipe.ability_count, 1)

    def test_remove_ability(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        self.assertTrue(pipe.remove_ability("a001"))
        self.assertEqual(pipe.ability_count, 0)

    def test_get_ability(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        self.assertIsNotNone(pipe.get_ability("a001"))

    def test_get_all_abilities(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry("a001"))
        pipe.add_ability(self._entry("a002"))
        self.assertEqual(len(pipe.get_all_abilities()), 2)

    def test_add_cost(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        cost = AbilityCostDef(cost_id="c001", cost_name="Mana Cost")
        self.assertTrue(pipe.add_cost("a001", cost))
        self.assertTrue(pipe.get_ability("a001").has_costs)

    def test_add_effect(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        effect = AbilityEffectDef(effect_id="e001", effect_name="Fireball Hit")
        self.assertTrue(pipe.add_effect("a001", effect))
        self.assertTrue(pipe.get_ability("a001").has_effects)

    def test_compile(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        self.assertTrue(pipe.compile("a001"))
        self.assertTrue(pipe.get_ability("a001").is_compiled)

    def test_compile_all(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry("a001"))
        pipe.add_ability(self._entry("a002"))
        results = pipe.compile_all()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(results.values()))

    def test_invalidate(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        pipe.compile("a001")
        pipe.invalidate("a001")
        self.assertFalse(pipe.get_ability("a001").is_compiled)

    def test_invalidate_all(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        pipe.compile("a001")
        pipe.invalidate_all()
        self.assertFalse(pipe.get_ability("a001").is_compiled)

    def test_get_uncompiled(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry("a001"))
        pipe.add_ability(self._entry("a002"))
        pipe.compile("a001")
        uncompiled = pipe.get_uncompiled()
        self.assertEqual(len(uncompiled), 1)

    def test_validate(self):
        pipe = self._pipeline()
        entry = self._entry()
        self.assertTrue(pipe.validate(entry))

    def test_ability_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.ability_count, 0)
        pipe.add_ability(self._entry())
        self.assertEqual(pipe.ability_count, 1)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_ability(self._entry())
        pipe.clear()
        self.assertTrue(pipe.is_empty)


# ---------------------------------------------------------------------------
# EQSGeneratorConfig
# ---------------------------------------------------------------------------

class TestEQSGeneratorConfig(unittest.TestCase):
    def test_generator_id(self):
        g = EQSGeneratorConfig(generator_id="g001", generator_name="Circle Gen")
        self.assertEqual(g.generator_id, "g001")

    def test_generator_name(self):
        g = EQSGeneratorConfig(generator_id="g001", generator_name="Circle Gen")
        self.assertEqual(g.generator_name, "Circle Gen")

    def test_default_generator_type(self):
        g = EQSGeneratorConfig(generator_id="g001", generator_name="Circle Gen")
        self.assertEqual(g.generator_type, "OnCircle")

    def test_default_radius(self):
        g = EQSGeneratorConfig(generator_id="g001", generator_name="Circle Gen")
        self.assertAlmostEqual(g.radius, 500.0)

    def test_is_enabled_true(self):
        g = EQSGeneratorConfig(generator_id="g001", generator_name="Circle Gen")
        self.assertTrue(g.is_enabled)

    def test_is_grid_false(self):
        g = EQSGeneratorConfig(generator_id="g001", generator_name="Circle Gen", generator_type="OnCircle")
        self.assertFalse(g.is_grid)


# ---------------------------------------------------------------------------
# EQSTestConfig
# ---------------------------------------------------------------------------

class TestEQSTestConfig(unittest.TestCase):
    def test_test_id(self):
        t = EQSTestConfig(test_id="t001", test_name="Distance Test")
        self.assertEqual(t.test_id, "t001")

    def test_test_name(self):
        t = EQSTestConfig(test_id="t001", test_name="Distance Test")
        self.assertEqual(t.test_name, "Distance Test")

    def test_default_test_type(self):
        t = EQSTestConfig(test_id="t001", test_name="Distance Test")
        self.assertEqual(t.test_type, "Distance")

    def test_default_weight(self):
        t = EQSTestConfig(test_id="t001", test_name="Distance Test")
        self.assertAlmostEqual(t.weight, 1.0)

    def test_is_enabled_true(self):
        t = EQSTestConfig(test_id="t001", test_name="Distance Test")
        self.assertTrue(t.is_enabled)

    def test_is_filtered_false(self):
        t = EQSTestConfig(test_id="t001", test_name="Distance Test")
        self.assertFalse(t.is_filtered)


# ---------------------------------------------------------------------------
# EQSQueryResult
# ---------------------------------------------------------------------------

class TestEQSQueryResult(unittest.TestCase):
    def test_job_id(self):
        r = EQSQueryResult(job_id="job001", query_id="q001")
        self.assertEqual(r.job_id, "job001")

    def test_query_id(self):
        r = EQSQueryResult(job_id="job001", query_id="q001")
        self.assertEqual(r.query_id, "q001")

    def test_has_results_false(self):
        r = EQSQueryResult(job_id="job001", query_id="q001")
        self.assertFalse(r.has_results)

    def test_item_count_zero(self):
        r = EQSQueryResult(job_id="job001", query_id="q001")
        self.assertEqual(r.item_count, 0)


# ---------------------------------------------------------------------------
# EnvironmentQueryPipeline
# ---------------------------------------------------------------------------

class TestEnvironmentQueryPipeline(unittest.TestCase):
    def _pipeline(self):
        return EnvironmentQueryPipeline()

    def test_add_query(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        self.assertEqual(pipe.query_count, 1)

    def test_remove_query(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        self.assertTrue(pipe.remove_query("q001"))
        self.assertEqual(pipe.query_count, 0)

    def test_get_query(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        self.assertIsNotNone(pipe.get_query("q001"))

    def test_get_all_queries(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        pipe.add_query("q002", "Find Enemy")
        self.assertEqual(len(pipe.get_all_queries()), 2)

    def test_add_generator(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        gen = EQSGeneratorConfig(generator_id="g001", generator_name="Circle Gen")
        self.assertTrue(pipe.add_generator("q001", gen))

    def test_add_test(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        test = EQSTestConfig(test_id="t001", test_name="Distance Test")
        self.assertTrue(pipe.add_test("q001", test))

    def test_run(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        result = pipe.run("q001")
        self.assertIsInstance(result, EQSQueryResult)

    def test_run_all(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        pipe.add_query("q002", "Find Enemy")
        results = pipe.run_all()
        self.assertEqual(len(results), 2)

    def test_validate(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        self.assertTrue(pipe.validate("q001"))

    def test_query_count(self):
        pipe = self._pipeline()
        self.assertEqual(pipe.query_count, 0)
        pipe.add_query("q001", "Find Cover")
        self.assertEqual(pipe.query_count, 1)

    def test_is_empty_true(self):
        pipe = self._pipeline()
        self.assertTrue(pipe.is_empty)

    def test_clear(self):
        pipe = self._pipeline()
        pipe.add_query("q001", "Find Cover")
        pipe.clear()
        self.assertTrue(pipe.is_empty)


if __name__ == "__main__":
    unittest.main()
