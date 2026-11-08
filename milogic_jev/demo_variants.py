"""Examples covering every major variant."""

from milogic_jev.variants import (
    FixedShellCatalog,
    NestedSubshellCatalog,
    OpenMonadBuilder,
    MultiMonadEvaluator,
    TemporalMonad,
    EvolutionarySelector,
    BoundedGrowthCatalog,
    ClosureComposer,
    MultiLevelState,
    DualityCalibrationLog,
    HybridOrchestrator,
)
from milogic_jev.core import build_belyaev_core_catalog


def mock(state, questions):
    out = {}
    for qid, q in questions.items():
        t = q.get("type")
        if t == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a", "a"),
                "dominance_probability": 0.7,
                "closure": 0.8,
                "generates_higher_level": True,
                "higher_level_confidence": 0.65,
                "relation_type": "complementary",
                "suggested_next_level": "следующий"
            }
        elif t == "score":
            out[qid] = {"value": 7.5, "confidence": 0.7}
        elif t == "noul":
            out[qid] = {"probability": 0.75, "answer": True}
        elif t == "choice":
            out[qid] = {"choice": q.get("options", ["x"])[0], "confidence": 0.6}
        else:
            out[qid] = {}
    return out


def demo_all():
    print("1. Fixed shells")
    fixed = FixedShellCatalog(max_levels=2)
    fixed.add_level("L0", {"q": {"type": "noul", "criteria": "test"}})
    fixed.add_level("L1", {"q2": {"type": "score", "min": 0, "max": 10, "criteria": "test"}})
    print(fixed.evaluate("state", mock))

    print("\n2. Nested subshell")
    nested = NestedSubshellCatalog()
    nested.add_question("base", {"type": "score", "min": 0, "max": 10, "criteria": "base"})
    print(nested.evaluate("state", mock))

    print("\n3. Open monad")
    print(OpenMonadBuilder.as_questions("замысел", "тест"))

    print("\n4. Multi-monad")
    mm = MultiMonadEvaluator([
        {"id": "fc", "pole_a": "форма", "pole_b": "содержание", "criteria": "тест"},
        {"id": "im", "pole_a": "замысел", "pole_b": "смысл", "criteria": "тест"},
    ])
    print(list(mm.build_questions().keys()))

    print("\n5. Temporal")
    print(list(TemporalMonad.as_questions("a", "b", "изменение").keys()))

    print("\n6. Evolutionary selector")
    sel = EvolutionarySelector()
    sel.add_candidate("формулировка A", [0.8, 0.82, 0.79])
    sel.add_candidate("формулировка B", [0.6, 0.9, 0.4])
    print(sel.best())

    print("\n7. Bounded growth")
    bg = BoundedGrowthCatalog(max_subshells_per_level=2)
    print("can add:", bg.can_add_subshell("L0"))

    print("\n8. Closure composer")
    comp = ClosureComposer()
    print(comp.compose(mock("s", {"m": {"type": "monad", "pole_a": "a", "pole_b": "b", "closure": 0.85}})))

    print("\n9. Multi-level state")
    mls = MultiLevelState()
    mls.add("L0", "водород")
    mls.add("L1", "периодическая система")
    print(mls.to_prompt())

    print("\n10. Calibration log")
    log = DualityCalibrationLog()
    log.log("форма", "содержание", 0.8, True)
    log.log("замысел", "смысл", 0.6, False)
    print(log.summary())

    print("\n11. Hybrid orchestrator")
    orch = HybridOrchestrator(build_belyaev_core_catalog())
    result = orch.run("водород → система", mock)
    print("suggestions:", len(result["suggestions"]))
    print("calibration:", result["calibration"])


if __name__ == "__main__":
    demo_all()
