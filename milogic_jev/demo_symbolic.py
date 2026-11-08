"""Demo of the symbolic / Tarot-style advisor."""

from milogic_jev.symbolic import (
    build_tarot_business_catalog,
    build_domain_catalog,
    SymbolicAdvisor,
)


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
            out[qid] = {
                "type": "monad",
                "pole_a": q.get("pole_a"),
                "pole_b": q.get("pole_b"),
                "dominant": q.get("pole_a"),
                "dominance_probability": 0.71,
                "closure": 0.79,
                "generates_higher_level": True,
                "higher_level_confidence": 0.66,
                "relation_type": "complementary",
                "suggested_next_level": "следующий уровень по образу и подобию"
            }
        elif q.get("type") == "score":
            out[qid] = {"value": 7.4, "confidence": 0.68}
        elif q.get("type") == "noul":
            out[qid] = {"probability": 0.73, "answer": True}
        elif q.get("type") == "choice":
            out[qid] = {"choice": q.get("options", ["?"])[0], "confidence": 0.65}
        else:
            out[qid] = {}
    return out


def demo():
    print("=== Tarot-style business advisor ===")
    advisor = SymbolicAdvisor(build_tarot_business_catalog(max_cards=3))
    result = advisor.advise(
        state="Сервисный бизнес: спрос растёт, команда не успевает, качество начинает проседать",
        evaluator=mock_evaluator
    )
    print(result["summary"])
    print("Действие:", result["action"])
    print("Следующий шаг:", result["next_step"])
    print("Предложений следующего уровня:", len(result.get("suggestions", [])))

    print("\n=== Domain catalog: trade ===")
    trade = SymbolicAdvisor(build_domain_catalog("trade"))
    r2 = trade.advise("Офлайн-магазин, онлайн-канал слабый, цена выше рынка", mock_evaluator)
    print(r2["summary"])

    print("\n=== Domain catalog: service ===")
    service = SymbolicAdvisor(build_domain_catalog("service"))
    r3 = service.advise("Консалтинг: экспертиза сильная, процессы хаотичные", mock_evaluator)
    print(r3["summary"])


if __name__ == "__main__":
    demo()
