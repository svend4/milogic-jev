"""
Concrete refinement generators that turn Kryukov structures
into ready-to-use sub-catalogs and questions.
"""

from typing import Dict, List, Any, Optional
from .core import HierarchicalCatalog, MonadAnswer
from .kryukov_extension import expand_monad_to_structure, STRUCTURES


def monad_to_subcatalog(monad: MonadAnswer, structure: str = "trefoil", level_prefix: str = "R") -> HierarchicalCatalog:
    expansion = expand_monad_to_structure(monad, structure)
    cat = HierarchicalCatalog(max_levels=2, closure_threshold=0.70)
    l0 = {}
    for i, variant in enumerate(expansion["sub_variants"]):
        key = f"{level_prefix}_{structure}_{i}"
        focus = variant.get("focus") or variant.get("size") or variant.get("sphere") or str(variant)
        l0[key] = {"type": "score", "min": 0, "max": 10, "criteria": f"Сила / ясность: {focus}"}
    cat.add_level(f"{level_prefix}_L0", l0, description=f"Уточнение ({structure}) для {monad.pole_a} ↔ {monad.pole_b}")
    cat.add_level(
        f"{level_prefix}_L1",
        questions={
            "next_focus": {
                "type": "choice",
                "options": [v.get("focus", str(v))[:80] for v in expansion["sub_variants"]],
                "criteria": "Какой подвариант сейчас приоритетен",
            }
        },
        condition=lambda ctx: True,
        description="Приоритет среди подвариантов",
    )
    return cat


def refine_all_strong(level_results: Dict, structure: str = "trefoil", min_closure: float = 0.65) -> List[Dict[str, Any]]:
    packages = []
    for level_name, level_res in level_results.items():
        if not hasattr(level_res, "monads"):
            continue
        for idx, monad in enumerate(level_res.monads):
            if not monad.is_strongly_closed(min_closure):
                continue
            sub = monad_to_subcatalog(monad, structure, level_prefix=f"{level_name}_{idx}")
            packages.append({
                "source_level": level_name,
                "base": f"{monad.pole_a} ↔ {monad.pole_b}",
                "closure": monad.closure,
                "structure": structure,
                "subcatalog": sub,
                "expansion": expand_monad_to_structure(monad, structure),
            })
    return packages


class RefinementOrchestrator:
    """Run a base catalog, then automatically generate refinement sub-catalogs."""
    def __init__(self, default_structure: str = "trefoil"):
        self.default_structure = default_structure

    def run(self, base_catalog: HierarchicalCatalog, state: str, evaluator, structure: Optional[str] = None, evaluate_sub: bool = False) -> Dict[str, Any]:
        structure = structure or self.default_structure
        base_results = base_catalog.evaluate(state, evaluator)
        packages = refine_all_strong(base_results, structure)
        output = {"base_results": base_results, "structure": structure, "refinements": []}
        for pkg in packages:
            entry = {
                "base": pkg["base"],
                "closure": pkg["closure"],
                "structure": pkg["structure"],
                "sub_variants": pkg["expansion"]["sub_variants"],
            }
            if evaluate_sub:
                sub_res = pkg["subcatalog"].evaluate(state, evaluator)
                entry["sub_results"] = {k: (v.reason if hasattr(v, "reason") else str(v)) for k, v in sub_res.items()}
            output["refinements"].append(entry)
        return output


def list_structures() -> Dict[str, Dict]:
    return STRUCTURES
