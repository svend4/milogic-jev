"""Demo of journal-aware pipeline."""

from milogic_jev.pipeline_journal import run_full_with_journal
from milogic_jev.journal import summary


def mock_evaluator(state: str, questions: dict) -> dict:
    out = {}
    for qid, q in questions.items():
        if q.get("type") == "monad":
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
                "suggested_next_level": "next",
            }
        else:
            out[qid] = {}
    return out


def demo():
    path = "session_journal.jsonl"
    res = run_full_with_journal(
        domain="services",
        state="Спрос растёт",
        evaluator=mock_evaluator,
        structure="trefoil",
        journal_path=path,
    )
    print(res["summary"])
    print("Recorded:", res["journal_recorded"])
    print("Journal:", summary(path))


if __name__ == "__main__":
    demo()
