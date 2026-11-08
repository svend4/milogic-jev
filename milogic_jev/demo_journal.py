"""Demo of journal and scene prompts."""

from milogic_jev.symbolic import SymbolicAdvisor, build_tarot_business_catalog
from milogic_jev.micro_archetypes import MicroArchetypeLayer
from milogic_jev.journal import JournalRecorder, summary
from milogic_jev.prompts import prompts_from_micro
from milogic_jev.carriers import build_carrier_catalog
from milogic_jev.carrier_scenes import CarrierSceneLayer
from milogic_jev.prompts import prompts_from_carriers


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.78,
                "closure": 0.82,
                "generates_higher_level": True,
                "higher_level_confidence": 0.70,
                "relation_type": "complementary",
                "suggested_next_level": "next",
            }
        else:
            out[qid] = {}
    return out


def demo():
    rec = JournalRecorder("demo_journal.jsonl")
    advisor = SymbolicAdvisor(build_tarot_business_catalog(max_cards=2))
    results = advisor.catalog.evaluate("test state", mock_evaluator)
    n = rec.record_results("tarot_demo", results)
    print(f"Recorded {n} entries")
    print("Summary:", summary("demo_journal.jsonl"))

    layer = MicroArchetypeLayer(max_gears=2)
    enriched = layer.enrich(results)
    prompts = prompts_from_micro(enriched)
    print("\nMicro prompts:")
    for p in prompts[:2]:
        print(" ", p[:120], "...")

    c_cat = build_carrier_catalog(max_carriers=2)
    c_adv = SymbolicAdvisor(c_cat)
    c_res = c_adv.catalog.evaluate("object", mock_evaluator)
    scenes = CarrierSceneLayer().enrich(c_res)
    c_prompts = prompts_from_carriers(scenes)
    print("\nCarrier prompts:")
    for p in c_prompts[:1]:
        print(" ", p[:120], "...")


if __name__ == "__main__":
    demo()
