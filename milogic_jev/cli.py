"""Simple CLI for milogic-jev."""

import argparse
import json

from .catalogs_extended import list_domains
from .carriers import list_carriers
from .pipeline_full import run_full
from .compare import compare_domains


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
                "closure": 0.78,
                "generates_higher_level": True,
                "higher_level_confidence": 0.65,
                "relation_type": "complementary",
                "suggested_next_level": "next",
            }
        else:
            out[qid] = {}
    return out


def cmd_domains(_args):
    print("\n".join(list_domains()))


def cmd_carriers(_args):
    print("\n".join(list_carriers()))


def cmd_run(args):
    res = run_full(
        domain=args.domain,
        state=args.state or "состояние не задано",
        evaluator=mock_evaluator,
        structure=args.structure,
        with_micro=not args.no_micro,
    )
    print(json.dumps(res["summary"], ensure_ascii=False, indent=2))
    if res.get("micro"):
        print("\nМикро-архетипы:")
        for m in res["micro"][:3]:
            print(f"  {m['monad']}")


def cmd_compare(args):
    d1, d2 = args.domains
    cmp = compare_domains(d1, d2)
    print(f"=== {cmp['domain_a']} ({cmp['count_a']}) ===")
    for p in cmp["poles_a"]:
        print(" ", p)
    print(f"\n=== {cmp['domain_b']} ({cmp['count_b']}) ===")
    for p in cmp["poles_b"]:
        print(" ", p)


def main():
    parser = argparse.ArgumentParser(prog="milogic-jev")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("domains").set_defaults(func=cmd_domains)
    sub.add_parser("carriers").set_defaults(func=cmd_carriers)

    p_run = sub.add_parser("run")
    p_run.add_argument("--domain", default="services")
    p_run.add_argument("--state", default="")
    p_run.add_argument("--structure", default="trefoil")
    p_run.add_argument("--no-micro", action="store_true")
    p_run.set_defaults(func=cmd_run)

    p_cmp = sub.add_parser("compare")
    p_cmp.add_argument("domains", nargs=2)
    p_cmp.set_defaults(func=cmd_compare)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
