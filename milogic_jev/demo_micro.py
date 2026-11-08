"""Demo of micro-archetypes ("gears") and game-style scenes."""

from milogic_jev.symbolic import SymbolicAdvisor, build_tarot_business_catalog
from milogic_jev.micro_archetypes import MicroArchetypeLayer


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.77,
                "closure": 0.83,
                "generates_higher_level": True,
                "higher_level_confidence": 0.71,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень",
            }
        else:
            out[qid] = {}
    return out


def demo():
    advisor = SymbolicAdvisor(build_tarot_business_catalog(max_cards=2))
    results = advisor.catalog.evaluate(
        "Консультация: клиент хочет расти, но боится потерять контроль",
        mock_evaluator,
    )

    layer = MicroArchetypeLayer(max_gears=3)
    enriched = layer.enrich(results)

    for item in enriched:
        print(f"\n=== {item['monad']} (closure {item['closure']:.2f}) ===")
        print("Шестерёнки:")
        for g in item["gears"]:
            print(f"  [{g['size']}] {g['name']} — {g['game_object']}")
        print("Сцена:")
        s = item["scene"]
        print(f"  {s['scene']}")
        print(f"  {s['character']}")
        print(f"  {s['tension']}")
        print(f"  {s['next_move']}")


if __name__ == "__main__":
    demo()
