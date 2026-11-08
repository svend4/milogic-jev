"""Demo of CLI and domain comparison."""

from milogic_jev.compare import compare_domains, all_domain_summary


def demo():
    print("Domain sizes:")
    for d, n in all_domain_summary().items():
        print(f"  {d}: {n} monads")

    print("\nCompare services vs trade:")
    cmp = compare_domains("services", "trade")
    print(f"  {cmp['domain_a']}: {cmp['count_a']}")
    print(f"  {cmp['domain_b']}: {cmp['count_b']}")
    print("  services poles:", cmp["poles_a"][:2])
    print("  trade poles:", cmp["poles_b"][:2])


if __name__ == "__main__":
    demo()
