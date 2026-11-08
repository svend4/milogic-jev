"""Demo of carrier catalog + alice-snov style scenes."""

from milogic_jev.carriers import build_carrier_catalog, list_carriers
from milogic_jev.symbolic import SymbolicAdvisor
from milogic_jev.carrier_scenes import CarrierSceneLayer


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.73,
                "closure": 0.79,
                "generates_higher_level": True,
                "higher_level_confidence": 0.66,
                "relation_type": "complementary",
                "suggested_next_level": "следующий носитель",
            }
        elif q.get("type") == "choice":
            opts = q.get("options", ["?"])
            out[qid] = {"choice": opts[0], "confidence": 0.64}
        else:
            out[qid] = {}
    return out


def demo():
    print("Carriers:", ", ".join(list_carriers()))
    print()

    cat = build_carrier_catalog(max_carriers=4)
    advisor = SymbolicAdvisor(cat)
    results = advisor.catalog.evaluate(
        "Объект без подписи. Первое чтение.",
        mock_evaluator,
    )

    layer = CarrierSceneLayer()
    scenes = layer.enrich(results)

    for s in scenes:
        print(s["scene"])
        print(f"  аппарат: {s['apparatus']} | zero: {s['zero']}")
        print(f"  {s['next']}")
        print()


if __name__ == "__main__":
    demo()
