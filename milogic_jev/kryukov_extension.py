"""
Kryukov-style extension layer for Milogic-Jev.

Goes beyond simple duality (2 poles) into higher-order structures:
- loops / figure-8
- 3 spheres
- deformed figure-8 / trefoil
- 4-petaled (clover / square)
- multi-petal "bouquet" of cycles

These act as refinement / sub-variant generators on top of existing monads.
"""

from typing import Dict, List, Any, Optional
from .core import HierarchicalCatalog, MonadAnswer


STRUCTURES = {
    "duality": {
        "order": 2,
        "description": "Простая двойственность (два полюса)",
        "example": "ресурсы ↔ действие"
    },
    "loop": {
        "order": 2,
        "description": "Замкнутая петля / круг",
        "example": "действие → результат → коррекция → действие"
    },
    "figure8": {
        "order": 2,
        "description": "Восьмёрка (два связанных цикла)",
        "example": "явное ↔ скрытое с переходом"
    },
    "trefoil": {
        "order": 3,
        "description": "Трилистник (три лепестка разного размера)",
        "example": "малый / средний / большой цикл"
    },
    "three_spheres": {
        "order": 3,
        "description": "Три сферы (МВС / СВС / БВС)",
        "example": "микро / среднее / макро"
    },
    "clover": {
        "order": 4,
        "description": "Клевер / квадрат (четыре лепестка)",
        "example": "четыре направления или четыре окна"
    },
    "four_windows": {
        "order": 4,
        "description": "4×4 = 16 состояний",
        "example": "комбинации четырёх базовых факторов"
    },
    "bouquet": {
        "order": "variable",
        "description": "Букет: несколько циклов разного размера и цвета",
        "example": "набор петель разной длительности и веса"
    },
}


def expand_monad_to_structure(monad: MonadAnswer, structure: str = "trefoil") -> Dict[str, Any]:
    if structure not in STRUCTURES:
        structure = "trefoil"
    info = STRUCTURES[structure]
    base = f"{monad.pole_a} ↔ {monad.pole_b}"
    result = {
        "base_monad": base,
        "structure": structure,
        "order": info["order"],
        "description": info["description"],
        "sub_variants": [],
    }
    if structure == "trefoil":
        result["sub_variants"] = [
            {"size": "малый", "focus": f"локальный цикл вокруг {monad.dominant or monad.pole_a}"},
            {"size": "средний", "focus": f"текущий уровень {base}"},
            {"size": "большой", "focus": f"переход на следующий уровень ({monad.suggested_next_level or 'новый'})"},
        ]
    elif structure == "three_spheres":
        result["sub_variants"] = [
            {"sphere": "МВС", "focus": "микро: конкретные действия и ресурсы"},
            {"sphere": "СВС", "focus": "среднее: процессы и связи"},
            {"sphere": "БВС", "focus": "макро: цель и контекст"},
        ]
    elif structure == "figure8":
        result["sub_variants"] = [
            {"loop": "явный", "focus": monad.pole_a},
            {"loop": "скрытый", "focus": monad.pole_b},
            {"crossing": "переход", "focus": "точка смены доминирования"},
        ]
    elif structure == "clover":
        result["sub_variants"] = [
            {"petal": 1, "focus": "инициация"},
            {"petal": 2, "focus": "развитие"},
            {"petal": 3, "focus": "замыкание"},
            {"petal": 4, "focus": "переход / новый цикл"},
        ]
    elif structure == "bouquet":
        result["sub_variants"] = [
            {"petal": "короткий", "weight": 0.3, "focus": "быстрый цикл"},
            {"petal": "средний", "weight": 0.5, "focus": "основной цикл"},
            {"petal": "длинный", "weight": 0.8, "focus": "долгий цикл"},
        ]
    else:
        result["sub_variants"] = [{"note": "базовая двойственность без расширения"}]
    return result


def build_refinement_catalog(base_catalog: HierarchicalCatalog, structure: str = "trefoil") -> Dict[str, Any]:
    return {
        "structure": structure,
        "note": "Используйте evaluate() базового каталога, затем expand_monad_to_structure() на сильных монадах",
        "available_structures": list(STRUCTURES.keys()),
    }


class StructureExpander:
    """Extension layer: takes results from any Milogic-Jev catalog and generates higher-order variants."""
    def __init__(self, default_structure: str = "trefoil"):
        self.default_structure = default_structure

    def expand_results(self, level_results: Dict, structure: Optional[str] = None) -> List[Dict[str, Any]]:
        structure = structure or self.default_structure
        expansions = []
        for level_name, level_res in level_results.items():
            if not hasattr(level_res, "monads"):
                continue
            for monad in level_res.monads:
                if monad.is_strongly_closed(0.65):
                    exp = expand_monad_to_structure(monad, structure)
                    exp["source_level"] = level_name
                    expansions.append(exp)
        return expansions

    def suggest_structures(self, closure: float) -> List[str]:
        if closure >= 0.85:
            return ["clover", "four_windows", "bouquet"]
        if closure >= 0.75:
            return ["trefoil", "three_spheres", "figure8"]
        if closure >= 0.60:
            return ["figure8", "loop"]
        return ["duality"]
