"""Extended pipeline with optional journal recording."""

from typing import Dict, Any, Optional, Callable
from .pipeline_full import run_full as _run_full
from .journal import JournalRecorder


def run_full_with_journal(
    domain: Optional[str] = None,
    carrier_mode: bool = False,
    state: str = "",
    evaluator: Callable = None,
    structure: str = "trefoil",
    evaluate_sub: bool = False,
    with_micro: bool = True,
    max_gears: int = 3,
    journal_path: Optional[str] = None,
) -> Dict[str, Any]:
    result = _run_full(
        domain=domain,
        carrier_mode=carrier_mode,
        state=state,
        evaluator=evaluator,
        structure=structure,
        evaluate_sub=evaluate_sub,
        with_micro=with_micro,
        max_gears=max_gears,
    )

    if journal_path:
        rec = JournalRecorder(journal_path)
        source = result["summary"].get("source", "unknown")
        from .symbolic import SymbolicAdvisor
        from .catalogs_extended import build_domain_catalog
        from .carriers import build_carrier_catalog
        if carrier_mode:
            base_cat = build_carrier_catalog(max_carriers=6)
        else:
            base_cat = build_domain_catalog(domain)
        advisor = SymbolicAdvisor(base_cat)
        base_results = advisor.catalog.evaluate(state, evaluator)
        n = rec.record_results(source, base_results)
        result["journal_recorded"] = n
    else:
        result["journal_recorded"] = 0

    return result
