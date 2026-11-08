"""Demo of the extended pipeline (domain + micro + optional carriers)."""

from milogic_jev.pipeline_full import run_full, available_structures


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        t = q.get("type")
        if t == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.76,
                "closure": 0.81,
                "generates_higher_level": True,
                "higher_level_confidence": 0.69,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень",
            }
        elif t == "choice":
            opts = q.get("options", ["?"])
            out[qid] = {"choice": opts[0], "confidence": 0.63}
        else:
            out[qid] = {}
    return out


def demo():
    print("Structures:", list(available_structures().keys()))
    print()

    res = run_full(
        domain="services",
        state="Спрос растёт, процессы не успевают",
        evaluator=mock_evaluator,
        structure="three_spheres",
        with_micro=True,
    )
    print("Services:", res["summary"])
    if res["micro"]:
        print("  micro example:", res["micro"][0]["monad"])

    res2 = run_full(
        carrier_mode=True,
        state="Объект без подписи",
        evaluator=mock_evaluator,
        structure="trefoil",
        with_micro=True,
    )
    print("\nCarriers:", res2["summary"])
    if res2["carrier_scenes"]:
        print("  scene:", res2["carrier_scenes"][0]["scene"][:80], "...")


if __name__ == "__main__":
    demo()
