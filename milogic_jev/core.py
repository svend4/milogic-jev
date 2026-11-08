"""
Milogic-Jev: New classes of decision systems
based on hierarchical dual relations (Milogiya) + structured questions (Jev).

This module implements the core new primitives and orchestrators.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable, Union
from enum import Enum
import json


class QuestionType(str, Enum):
    NOUL = "noul"
    CHOICE = "choice"
    SCORE = "score"
    MONAD = "monad"


class RelationType(str, Enum):
    COMPLEMENTARY = "complementary"
    ANTAGONISTIC = "antagonistic"
    TRANSITIONAL = "transitional"
    UNSTABLE = "unstable"


@dataclass
class MonadAnswer:
    """New primitive: dual relation evaluation."""
    pole_a: str
    pole_b: str
    dominant: str
    dominance_probability: float
    closure: float                    # 0.0–1.0
    generates_higher_level: bool
    higher_level_confidence: float
    relation_type: RelationType
    suggested_next_level: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def is_strongly_closed(self, threshold: float = 0.78) -> bool:
        return self.closure >= threshold and self.generates_higher_level


@dataclass
class LevelResult:
    level_id: str
    answers: Dict[str, Any]
    monads: List[MonadAnswer] = field(default_factory=list)
    can_proceed: bool = True
    reason: str = ""


class HierarchicalCatalog:
    """
    Class 1 + 5 + 6: Hierarchical shells with closure-driven progression.
    """
    def __init__(self, max_levels: int = 4, closure_threshold: float = 0.78):
        self.levels: List[Dict[str, Any]] = []
        self.max_levels = max_levels
        self.closure_threshold = closure_threshold

    def add_level(
        self,
        level_id: str,
        questions: Dict[str, Dict],
        condition: Optional[Callable[[Dict], bool]] = None,
        description: str = ""
    ):
        self.levels.append({
            "id": level_id,
            "questions": questions,
            "condition": condition,
            "description": description
        })

    def evaluate(self, state: str, evaluator: Callable) -> Dict[str, LevelResult]:
        context: Dict[str, Any] = {"original_state": state}
        results: Dict[str, LevelResult] = {}

        for i, level in enumerate(self.levels):
            if i >= self.max_levels:
                break

            if level["condition"] and not level["condition"](context):
                results[level["id"]] = LevelResult(
                    level_id=level["id"],
                    answers={},
                    can_proceed=False,
                    reason="condition not met"
                )
                break

            full_state = self._compose_state(context)
            raw_answers = evaluator(full_state, level["questions"])

            monads = self._extract_monads(raw_answers)
            can_proceed = self._should_continue(monads, raw_answers)

            level_result = LevelResult(
                level_id=level["id"],
                answers=raw_answers,
                monads=monads,
                can_proceed=can_proceed,
                reason="closure sufficient" if can_proceed else "closure too weak"
            )
            results[level["id"]] = level_result
            context[level["id"]] = raw_answers

            if not can_proceed:
                break

        return results

    def _compose_state(self, context: Dict) -> str:
        parts = [f"Исходное состояние:\n{context['original_state']}"]
        for key, value in context.items():
            if key == "original_state":
                continue
            parts.append(f"\n--- Результаты уровня {key} ---\n{json.dumps(value, ensure_ascii=False, indent=2)}")
        return "\n".join(parts)

    def _extract_monads(self, answers: Dict) -> List[MonadAnswer]:
        monads = []
        for qid, ans in answers.items():
            if isinstance(ans, dict) and ans.get("type") == "monad":
                monads.append(MonadAnswer(
                    pole_a=ans.get("pole_a", ""),
                    pole_b=ans.get("pole_b", ""),
                    dominant=ans.get("dominant", ""),
                    dominance_probability=ans.get("dominance_probability", 0.0),
                    closure=ans.get("closure", 0.0),
                    generates_higher_level=ans.get("generates_higher_level", False),
                    higher_level_confidence=ans.get("higher_level_confidence", 0.0),
                    relation_type=RelationType(ans.get("relation_type", "unstable")),
                    suggested_next_level=ans.get("suggested_next_level"),
                    raw=ans
                ))
        return monads

    def _should_continue(self, monads: List[MonadAnswer], answers: Dict) -> bool:
        if not monads:
            scores = [v.get("value", 0) for v in answers.values() if isinstance(v, dict) and "value" in v]
            return any(s >= 7 for s in scores) if scores else True
        return any(m.is_strongly_closed(self.closure_threshold) for m in monads)


class MonadQuestionBuilder:
    """Helper to construct monad questions from standard Jev types."""
    @staticmethod
    def as_jev_questions(pole_a: str, pole_b: str, criteria: str) -> Dict[str, Dict]:
        return {
            "dominant": {
                "type": "choice",
                "options": [pole_a, pole_b, "равновесие", "неопределённо"],
                "criteria": f"Какой полюс доминирует в отношении '{pole_a}' ↔ '{pole_b}'. {criteria}"
            },
            "closure": {
                "type": "score",
                "min": 0,
                "max": 10,
                "criteria": f"Насколько сильно и устойчиво замкнулось отношение. {criteria}"
            },
            "generates_higher": {
                "type": "noul",
                "criteria": f"Порождает ли это отношение осмысленный следующий уровень иерархии. {criteria}"
            },
            "relation_type": {
                "type": "choice",
                "options": ["complementary", "antagonistic", "transitional", "unstable"],
                "criteria": "Тип двойственного отношения"
            }
        }

    @staticmethod
    def from_jev_answers(pole_a: str, pole_b: str, answers: Dict) -> MonadAnswer:
        dominant_ans = answers.get("dominant", {})
        closure_ans = answers.get("closure", {})
        gen_ans = answers.get("generates_higher", {})
        rel_ans = answers.get("relation_type", {})

        closure_score = closure_ans.get("value", 0) / 10.0
        generates = gen_ans.get("probability", 0) > 0.6 or gen_ans.get("answer", False)

        return MonadAnswer(
            pole_a=pole_a,
            pole_b=pole_b,
            dominant=dominant_ans.get("choice", "неопределённо"),
            dominance_probability=dominant_ans.get("confidence", 0.5),
            closure=closure_score,
            generates_higher_level=bool(generates),
            higher_level_confidence=gen_ans.get("probability", 0.0),
            relation_type=RelationType(rel_ans.get("choice", "unstable")),
            suggested_next_level=None
        )


class ReferenceFrameEvaluator:
    """Class 4: Run the same state through multiple frames."""
    def __init__(self):
        self.frames: Dict[str, Dict] = {}

    def add_frame(self, name: str, questions: Dict):
        self.frames[name] = questions

    def evaluate(self, state: str, evaluator: Callable) -> Dict[str, Any]:
        results = {}
        confidences = []
        for name, questions in self.frames.items():
            ans = evaluator(state, questions)
            results[name] = ans
            conf = self._avg_confidence(ans)
            confidences.append((name, conf))

        best = max(confidences, key=lambda x: x[1]) if confidences else (None, 0)
        return {
            "frames": results,
            "best_frame": best[0],
            "best_confidence": best[1]
        }

    def _avg_confidence(self, answers: Dict) -> float:
        vals = []
        for a in answers.values():
            if isinstance(a, dict):
                if "confidence" in a:
                    vals.append(a["confidence"])
                elif "probability" in a:
                    vals.append(a["probability"])
                elif "value" in a:
                    vals.append(a["value"] / 10.0)
        return sum(vals) / len(vals) if vals else 0.0


class GenerativeCatalog:
    """Class 3: Suggest next-level questions based on strong closures."""
    def suggest_from_monad(self, monad: MonadAnswer) -> Optional[Dict]:
        if not monad.is_strongly_closed():
            return None
        next_pole = monad.suggested_next_level or f"следующий уровень от '{monad.dominant}'"
        return {
            "id": f"gen_{hash(monad.pole_a + monad.pole_b) % 10000}",
            "type": "monad",
            "pole_a": next_pole,
            "pole_b": "ещё более высокий уровень по образу и подобию",
            "criteria": (
                f"Оценить, является ли '{next_pole}' естественным продолжением "
                f"монады '{monad.pole_a}' ↔ '{monad.pole_b}' "
                f"(closure={monad.closure:.2f})"
            )
        }


def build_belyaev_core_catalog() -> HierarchicalCatalog:
    cat = HierarchicalCatalog(max_levels=3, closure_threshold=0.75)

    cat.add_level(
        "L0_basis",
        questions={
            "hydrogen_monad": {
                "type": "monad",
                "pole_a": "атом водорода (замысел)",
                "pole_b": "периодическая система (смысл)",
                "criteria": "Является ли атом водорода достаточным базисом для порождения периодической системы по милогии"
            }
        },
        description="Базисная двойственность"
    )

    def l1_condition(ctx):
        l0 = ctx.get("L0_basis", {})
        m = l0.get("hydrogen_monad", {}) if isinstance(l0, dict) else {}
        return m.get("closure", 0) >= 0.6

    cat.add_level(
        "L1_periodic",
        questions={
            "periodic_as_shell": {
                "type": "score",
                "min": 0,
                "max": 10,
                "criteria": "Насколько периодическая система является замкнутой оболочкой 2-го уровня иерархии"
            },
            "nuclear_potential": {
                "type": "noul",
                "criteria": "Ядерные оболочки естественно следуют как следующий уровень"
            }
        },
        condition=l1_condition,
        description="Замыкание в периодическую систему"
    )

    return cat
