"""Unified pipeline: domain → base monads → Kryukov refinement."""

from typing import Dict, Any, Optional, Callable
from .catalogs_extended import build_domain_catalog, list_domains
from .symbolic import SymbolicAdvisor
from .refinement import RefinementOrchestrator
from .kryukov_extension import STRUCTURES


def run_domain_with_refinement(domain: str, state: str, evaluator: Callable, structure: str = "trefoil", evaluate_sub: bool = False) -> Dict[str, Any]:
    if domain not in list_domains():
        raise ValueError(f"Unknown domain '{domain}'. Available: {list_domains()}")
    base_cat = build_domain_catalog(domain)
    orch = RefinementOrchestrator(default_structure=structure)
    result = orch.run(base_catalog=base_cat, state=state, evaluator=evaluator, structure=structure, evaluate_sub=evaluate_sub)
    strong = [r for r in result["refinements"] if r.get("closure", 0) >= 0.70]
    result["summary"] = {
        "domain": domain,
        "structure": structure,
        "strong_monads": len(strong),
        "recommendation": "действовать" if strong else "уточнять",
    }
    return result


def available_structures() -> Dict[str, str]:
    return {k: v["description"] for k, v in STRUCTURES.items()}


class DomainPipeline:
    """Convenience wrapper with a fixed domain and structure."""
    def __init__(self, domain: str, structure: str = "trefoil"):
        self.domain = domain
        self.structure = structure

    def run(self, state: str, evaluator: Callable, evaluate_sub: bool = False) -> Dict[str, Any]:
        return run_domain_with_refinement(domain=self.domain, state=state, evaluator=evaluator, structure=self.structure, evaluate_sub=evaluate_sub)
