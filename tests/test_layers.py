"""Basic tests for refinement and carrier layers."""

import unittest
from milogic_jev.carriers import build_carrier_catalog, list_carriers, get_carrier
from milogic_jev.refinement import monad_to_subcatalog
from milogic_jev.core import MonadAnswer
from milogic_jev.micro_archetypes import attach_micro_archetypes


class TestCarriers(unittest.TestCase):
    def test_list(self):
        ids = list_carriers()
        self.assertGreaterEqual(len(ids), 10)
        self.assertIn("ski_rocker", ids)

    def test_get(self):
        c = get_carrier("hat")
        self.assertEqual(c["mode_a"], "надеть")
        self.assertIn("zero", c)

    def test_catalog(self):
        cat = build_carrier_catalog(max_carriers=3)
        level_ids = [lv["id"] for lv in cat.levels]
        self.assertIn("L0_carriers", level_ids)


class TestMicro(unittest.TestCase):
    def test_attach(self):
        m = MonadAnswer(
            pole_a="A", pole_b="B", dominant="A",
            dominance_probability=0.8, closure=0.85,
            generates_higher_level=True, higher_level_confidence=0.7,
            relation_type="complementary", suggested_next_level="next",
        )
        gears = attach_micro_archetypes(m, max_gears=3)
        self.assertEqual(len(gears), 3)
        self.assertIn("name", gears[0])


class TestRefinement(unittest.TestCase):
    def test_trefoil(self):
        m = MonadAnswer(
            pole_a="A", pole_b="B", dominant="A",
            dominance_probability=0.8, closure=0.85,
            generates_higher_level=True, higher_level_confidence=0.7,
            relation_type="complementary", suggested_next_level="next",
        )
        sub = monad_to_subcatalog(m, structure="trefoil")
        self.assertTrue(hasattr(sub, "levels") or isinstance(sub, dict))


if __name__ == "__main__":
    unittest.main()
