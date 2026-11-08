"""
Lightweight tests that do not require a live Jev API.
Run with: python -m pytest tests/   or   python tests/test_core.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from milogic_jev.core import (
    HierarchicalCatalog,
    MonadQuestionBuilder,
    GenerativeCatalog,
    MonadAnswer,
    RelationType,
    build_belyaev_core_catalog,
)
from milogic_jev.catalogs import get_symmetry_dualities, as_jev_questions


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.7,
                "closure": 0.82,
                "generates_higher_level": True,
                "higher_level_confidence": 0.7,
                "relation_type": "complementary",
                "suggested_next_level": "next",
            }
        elif q.get("type") == "score":
            out[qid] = {"value": 8.0}
        elif q.get("type") == "noul":
            out[qid] = {"probability": 0.8, "answer": True}
        elif q.get("type") == "choice":
            opts = q.get("options", [])
            choice = "complementary" if "complementary" in opts else (opts[0] if opts else "равновесие")
            out[qid] = {"choice": choice, "confidence": 0.6}
        else:
            out[qid] = {}
    return out


def test_belyaev_catalog_runs():
    cat = build_belyaev_core_catalog()
    result = cat.evaluate("водород и периодическая система", mock_evaluator)
    assert "L0_basis" in result
    assert result["L0_basis"].can_proceed is True


def test_monad_builder_roundtrip():
    builder = MonadQuestionBuilder()
    qs = builder.as_jev_questions("форма", "содержание", "тест")
    answers = mock_evaluator("state", qs)
    monad = builder.from_jev_answers("форма", "содержание", answers)
    assert isinstance(monad, MonadAnswer)
    assert 0.0 <= monad.closure <= 1.0


def test_generative_suggests_on_strong_closure():
    gen = GenerativeCatalog()
    m = MonadAnswer(
        pole_a="a",
        pole_b="b",
        dominant="a",
        dominance_probability=0.8,
        closure=0.85,
        generates_higher_level=True,
        higher_level_confidence=0.7,
        relation_type=RelationType.COMPLEMENTARY,
        suggested_next_level="уровень N+1",
    )
    suggestion = gen.suggest_from_monad(m)
    assert suggestion is not None
    assert "уровень N+1" in suggestion["pole_a"]


def test_generative_skips_weak_closure():
    gen = GenerativeCatalog()
    m = MonadAnswer(
        pole_a="a",
        pole_b="b",
        dominant="a",
        dominance_probability=0.5,
        closure=0.4,
        generates_higher_level=False,
        higher_level_confidence=0.3,
        relation_type=RelationType.UNSTABLE,
    )
    assert gen.suggest_from_monad(m) is None


def test_symmetry_dualities_exist():
    duals = get_symmetry_dualities()
    assert len(duals) >= 4
    qs = as_jev_questions(duals[0])
    assert duals[0]["id"] in qs


def test_condition_blocks_level():
    cat = HierarchicalCatalog(max_levels=2, closure_threshold=0.9)
    cat.add_level("L0", {"q": {"type": "noul", "criteria": "test"}})
    cat.add_level(
        "L1",
        {"q2": {"type": "score", "min": 0, "max": 10, "criteria": "test"}},
        condition=lambda ctx: False,
    )
    result = cat.evaluate("state", mock_evaluator)
    assert "L0" in result
    assert result.get("L1") is None or result["L1"].can_proceed is False


if __name__ == "__main__":
    test_belyaev_catalog_runs()
    test_monad_builder_roundtrip()
    test_generative_suggests_on_strong_closure()
    test_generative_skips_weak_closure()
    test_symmetry_dualities_exist()
    test_condition_blocks_level()
    print("All tests passed.")
