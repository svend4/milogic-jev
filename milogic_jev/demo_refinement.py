"""Demo of automatic refinement into Kryukov structures."""

from milogic_jev.symbolic import SymbolicAdvisor, build_tarot_business_catalog
from milogic_jev.refinement import RefinementOrchestrator, list_structures


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
                "closure": 0.82,
                "generates_higher_level": True,
                "higher_level_confidence": 0.70,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень",
            }
        elif t == "score":
            out[qid] = {"value": 7.8, "confidence": 0.71}
        elif t == "choice":
            opts = q.get("options", ["?"])
            out[qid] = {"choice": opts[0], "confidence": 0.67}
        else:
            out[qid] = {}
    return out


def demo():
    print("Structures:", ", ".join(list_structures().keys()))
    print()

    advisor = SymbolicAdvisor(build_tarot_business_catalog(max_cards=2))
    orch = RefinementOrchestrator(default_structure="trefoil")

    result = orch.run(
        base_catalog=advisor.catalog,
        state="Сервисный бизнес: спрос растёт, процессы не успевают",
        evaluator=mock_evaluator,
        evaluate_sub=True,
    )

    print(f"Structure used: {result['structure']}")
    print(f"Refinements generated: {len(result['refinements'])}")
    for r in result["refinements"]:
        print(f"\n{r['base']}  (closure {r['closure']:.2f})")
        for v in r["sub_variants"]:
            print("  -", v)
        if "sub_results" in r:
            print("  sub-results:", list(r["sub_results"].keys()))


if __name__ == "__main__":
    demo()
