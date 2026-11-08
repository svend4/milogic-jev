"""
Example usage of Milogic-Jev classes.
Replace mock_evaluator with a real Jev (or compatible) API call.
"""

import json
from milogic_jev.core import (
    HierarchicalCatalog,
    MonadQuestionBuilder,
    GenerativeCatalog,
    build_belyaev_core_catalog,
    MonadAnswer,
    RelationType,
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
                "dominance_probability": 0.72,
                "closure": 0.81,
                "generates_higher_level": True,
                "higher_level_confidence": 0.68,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень по образу и подобию"
            }
        elif q.get("type") == "score":
            out[qid] = {"value": 7.8, "confidence": 0.7}
        elif q.get("type") == "noul":
            out[qid] = {"probability": 0.74, "answer": True}
        elif q.get("type") == "choice":
            out[qid] = {"choice": q.get("options", ["?"])[0], "confidence": 0.65}
        else:
            out[qid] = {"raw": "unsupported"}
    return out


def example_belyaev_core():
    print("=== Belyaev core catalog ===")
    catalog = build_belyaev_core_catalog()
    result = catalog.evaluate(
        state="Вкладывая в замысел смысл атома водорода, получаем закон эволюции периодической системы.",
        evaluator=mock_evaluator
    )
    for level_id, level_res in result.items():
        print(f"{level_id}: can_proceed={level_res.can_proceed}, reason={level_res.reason}")


def example_symmetry_dualities():
    print("\n=== Symmetry dualities ===")
    gen = GenerativeCatalog()
    for d in get_symmetry_dualities():
        questions = as_jev_questions(d)
        answers = mock_evaluator("общий контекст милогии", questions)
        raw = answers[d["id"]]
        print(f"{d['id']}: closure={raw.get('closure')}")
        m = MonadAnswer(
            pole_a=raw["pole_a"],
            pole_b=raw["pole_b"],
            dominant=raw["dominant"],
            dominance_probability=raw["dominance_probability"],
            closure=raw["closure"],
            generates_higher_level=raw["generates_higher_level"],
            higher_level_confidence=raw["higher_level_confidence"],
            relation_type=RelationType(raw["relation_type"]),
            suggested_next_level=raw.get("suggested_next_level")
        )
        suggestion = gen.suggest_from_monad(m)
        if suggestion:
            print(f"  → suggested: {suggestion['pole_a']}")


if __name__ == "__main__":
    example_belyaev_core()
    example_symmetry_dualities()
