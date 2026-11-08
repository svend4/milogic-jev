"""Extended pipeline: domain → monads → refinement → micro-archetypes → optional carriers."""

from typing import Dict, Any, Optional, Callable
from .catalogs_extended import build_domain_catalog, list_domains
from .symbolic import SymbolicAdvisor
from .refinement import RefinementOrchestrator
from .micro_archetypes import MicroArchetypeLayer
from .carriers import build_carrier_catalog
from .carrier_scenes import CarrierSceneLayer
from .kryukov_extension import STRUCTURES


def run_full(
    domain: Optional[str] = None,
    carrier_mode: bool = False,
    state: str = "",
    evaluator: Callable = None,
    structure: str = "trefoil",
    evaluate_sub: bool = False,
    with_micro: bool = True,
    max_gears: int = 3,
) -> Dict[str, Any]:
    if carrier_mode:
        base_cat = build_carrier_catalog(max_carriers=6)
        source = "carriers"
    else:
        if domain not in list_domains():
            raise ValueError(f"Unknown domain '{domain}'. Available: {list_domains()}")
        base_cat = build_domain_catalog(domain)
        source = domain

    orch = RefinementOrchestrator(default_structure=structure)
    result = orch.run(
        base_catalog=base_cat,
        state=state,
        evaluator=evaluator,
        structure=structure,
        evaluate_sub=evaluate_sub,
    )

    micro_items = []
    if with_micro:
        advisor = SymbolicAdvisor(base_cat)
        base_results = advisor.catalog.evaluate(state, evaluator)
        micro_items = MicroArchetypeLayer(max_gears=max_gears).enrich(base_results)

    carrier_scenes = []
    if carrier_mode:
        advisor = SymbolicAdvisor(base_cat)
        base_results = advisor.catalog.evaluate(state, evaluator)
        carrier_scenes = CarrierSceneLayer().enrich(base_results)

    strong = [r for r in result.get("refinements", []) if r.get("closure", 0) >= 0.70]

    result["summary"] = {
        "source": source,
        "structure": structure,
        "strong_monads": len(strong),
        "recommendation": "действовать" if strong else "уточнять",
        "micro_count": len(micro_items),
        "carrier_scenes": len(carrier_scenes),
    }
    result["micro"] = micro_items
    result["carrier_scenes"] = carrier_scenes
    return result


def available_structures() -> Dict[str, str]:
    return {k: v["description"] for k, v in STRUCTURES.items()}
