"""Domain comparison utility."""

from typing import Dict, List, Tuple
from .catalogs_extended import build_domain_catalog, list_domains


def extract_poles(domain: str) -> List[Tuple[str, str]]:
    cat = build_domain_catalog(domain)
    poles = []
    for lv in cat.levels:
        for qid, q in lv.get("questions", {}).items():
            if q.get("type") == "monad":
                poles.append((q.get("pole_a", ""), q.get("pole_b", "")))
    return poles


def compare_domains(d1: str, d2: str) -> Dict:
    p1 = extract_poles(d1)
    p2 = extract_poles(d2)
    return {
        "domain_a": d1,
        "domain_b": d2,
        "count_a": len(p1),
        "count_b": len(p2),
        "poles_a": [f"{a} ↔ {b}" for a, b in p1],
        "poles_b": [f"{a} ↔ {b}" for a, b in p2],
    }


def all_domain_summary() -> Dict[str, int]:
    return {d: len(extract_poles(d)) for d in list_domains()}
