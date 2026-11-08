"""
Milogic-Jev: New classes of decision systems
based on hierarchical dual relations (Milogiya) + structured questions (Jev).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import json


class RelationType(str, Enum):
    COMPLEMENTARY = "complementary"
    ANTAGONISTIC = "antagonistic"
    TRANSITIONAL = "transitional"
    UNSTABLE = "unstable"


@dataclass
class MonadAnswer:
    pole_a: str
    pole_b: str
    dominant: str
    dominance_probability: float
    closure: float
    generates_higher_level: bool
    higher_level_confidence: float
    relation_type: RelationType
    suggested_next_level: Optional[str] = None

    def is_strongly_closed(self, threshold: float = 0.78) -> bool:
        return self.closure >= threshold and self.generates_higher_level


class HierarchicalCatalog:
    def __init__(self, max_levels: int = 4, closure_threshold: float = 0.78):
        self.levels: List[Dict[str, Any]] = []
        self.max_levels = max_levels
        self.closure_threshold = closure_threshold

    def add_level(self, level_id: str, questions: Dict[str, Dict], condition: Optional[Callable] = None, description: str = ""):
        self.levels.append({"id": level_id, "questions": questions, "condition": condition, "description": description})

    def evaluate(self, state: str, evaluator: Callable) -> Dict[str, Any]:
        context = {"original_state": state}
        results = {}
        for i, level in enumerate(self.levels):
            if i >= self.max_levels:
                break
            if level["condition"] and not level["condition"](context):
                results[level["id"]] = {"can_proceed": False, "reason": "condition not met"}
                break
            full_state = self._compose_state(context)
            raw = evaluator(full_state, level["questions"])
            results[level["id"]] = raw
            context[level["id"]] = raw
            if not self._should_continue(raw):
                break
        return results

    def _compose_state(self, context: Dict) -> str:
        parts = [context["original_state"]]
        for k, v in context.items():
            if k != "original_state":
                parts.append(f"\n--- {k} ---\n{json.dumps(v, ensure_ascii=False)}")
        return "\n".join(parts)

    def _should_continue(self, answers: Dict) -> bool:
        for ans in answers.values():
            if isinstance(ans, dict) and ans.get("type") == "monad":
                if ans.get("closure", 0) >= self.closure_threshold and ans.get("generates_higher_level"):
                    return True
        return False


class MonadQuestionBuilder:
    @staticmethod
    def as_jev_questions(pole_a: str, pole_b: str, criteria: str) -> Dict:
        return {
            "dominant": {"type": "choice", "options": [pole_a, pole_b, "равновесие"], "criteria": f"Доминирующий полюс '{pole_a}' ↔ '{pole_b}'. {criteria}"},
            "closure": {"type": "score", "min": 0, "max": 10, "criteria": f"Сила замыкания. {criteria}"},
            "generates_higher": {"type": "noul", "criteria": f"Порождает ли следующий уровень. {criteria}"}
        }


def build_belyaev_core_catalog() -> HierarchicalCatalog:
    cat = HierarchicalCatalog(max_levels=3, closure_threshold=0.75)
    cat.add_level("L0_basis", {
        "hydrogen_monad": {
            "type": "monad",
            "pole_a": "атом водорода (замысел)",
            "pole_b": "периодическая система (смысл)",
            "criteria": "Достаточен ли атом водорода как базис для периодической системы"
        }
    })
    return cat
