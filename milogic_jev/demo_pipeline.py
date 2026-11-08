"""Demo of the unified domain → refinement pipeline."""

from milogic_jev.pipeline import run_domain_with_refinement, available_structures, DomainPipeline


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
                "dominance_probability": 0.75,
                "closure": 0.80,
                "generates_higher_level": True,
                "higher_level_confidence": 0.68,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень",
            }
        elif t == "score":
            out[qid] = {"value": 7.4, "confidence": 0.70}
        elif t == "choice":
            opts = q.get("options", ["?"])
            out[qid] = {"choice": opts[0], "confidence": 0.65}
        else:
            out[qid] = {}
    return out


def demo():
    print("Structures:")
    for k, v in available_structures().items():
        print(f"  {k}: {v}")
    print()

    res = run_domain_with_refinement(
        domain="services",
        state="Спрос растёт, процессы не успевают",
        evaluator=mock_evaluator,
        structure="three_spheres",
        evaluate_sub=True,
    )
    print(res["summary"])
    print(f"Refinements: {len(res['refinements'])}")
    for r in res["refinements"][:2]:
        print(" ", r["base"], "→", [v.get("focus") or v.get("sphere") for v in r["sub_variants"]])

    pipe = DomainPipeline(domain="trade", structure="trefoil")
    res2 = pipe.run("Новый канал продаж, старый ещё жив", mock_evaluator)
    print("\nTrade pipeline:", res2["summary"])


if __name__ == "__main__":
    demo()
