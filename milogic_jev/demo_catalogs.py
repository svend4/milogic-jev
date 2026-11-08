"""Demo of extended domain and system catalogs."""

from milogic_jev.catalogs_extended import (
    list_domains,
    build_domain_catalog,
    build_iching_catalog,
    build_social_catalog,
)
from milogic_jev.symbolic import SymbolicAdvisor


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.68,
                "closure": 0.76,
                "generates_higher_level": True,
                "higher_level_confidence": 0.62,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень",
            }
        elif q.get("type") == "choice":
            out[qid] = {"choice": q.get("options", ["?"])[0], "confidence": 0.64}
        elif q.get("type") == "score":
            out[qid] = {"value": 7.2, "confidence": 0.67}
        elif q.get("type") == "noul":
            out[qid] = {"probability": 0.71, "answer": True}
        else:
            out[qid] = {}
    return out


def demo():
    print("Available domains:", ", ".join(list_domains()))
    print()

    for domain in ["trade", "services", "it_digital", "finance", "personal_project"]:
        advisor = SymbolicAdvisor(build_domain_catalog(domain))
        result = advisor.advise(f"Ситуация в сфере {domain}", mock_evaluator)
        print(f"[{domain}] {result['summary']}")

    print()
    iching = SymbolicAdvisor(build_iching_catalog())
    print("[I Ching]", iching.advise("Проект на этапе роста", mock_evaluator)["summary"])

    social = SymbolicAdvisor(build_social_catalog())
    print("[Social]", social.advise("Команда, формальные процессы слабые", mock_evaluator)["summary"])


if __name__ == "__main__":
    demo()
