"""Demo of the Kryukov-style extension layer."""

from milogic_jev.symbolic import SymbolicAdvisor, build_tarot_business_catalog
from milogic_jev.kryukov_extension import StructureExpander, STRUCTURES


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.74,
                "closure": 0.81,
                "generates_higher_level": True,
                "higher_level_confidence": 0.69,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень",
            }
        else:
            out[qid] = {}
    return out


def demo():
    print("Available structures:")
    for name, info in STRUCTURES.items():
        print(f"  {name:16} order={info['order']:<8} {info['description']}")

    print("\n=== Expanding strong monads ===")
    advisor = SymbolicAdvisor(build_tarot_business_catalog(max_cards=2))
    results = advisor.catalog.evaluate(
        "Бизнес растёт, но процессы не успевают",
        mock_evaluator
    )

    expander = StructureExpander()
    for structure in ["trefoil", "three_spheres", "figure8", "clover"]:
        print(f"\n--- structure: {structure} ---")
        expansions = expander.expand_results(results, structure=structure)
        for exp in expansions:
            print(exp["base_monad"])
            for v in exp["sub_variants"]:
                print(" ", v)


if __name__ == "__main__":
    demo()
