"""
Extended implementations of all Milogic-Jev class variants.
Each class from the taxonomy is given concrete, usable code.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
import json
import statistics

from .core import (
    HierarchicalCatalog,
    GenerativeCatalog,
    ReferenceFrameEvaluator,
)


class FixedShellCatalog(HierarchicalCatalog):
    """1.1 Fixed shells — levels always run in order."""
    def evaluate(self, state: str, evaluator: Callable) -> Dict[str, Any]:
        context = {"original_state": state}
        results = {}
        for level in self.levels[: self.max_levels]:
            full_state = self._compose_state(context)
            raw = evaluator(full_state, level["questions"])
            results[level["id"]] = raw
            context[level["id"]] = raw
        return results


class NestedSubshellCatalog:
    """1.3 Nested subshells."""
    def __init__(self):
        self.questions: Dict[str, Dict] = {}

    def add_question(self, qid: str, question: Dict, subshell: Optional["NestedSubshellCatalog"] = None):
        self.questions[qid] = {"question": question, "subshell": subshell}

    def evaluate(self, state: str, evaluator: Callable) -> Dict[str, Any]:
        results = {}
        for qid, item in self.questions.items():
            ans = evaluator(state, {qid: item["question"]})
            results[qid] = ans.get(qid, ans)
            if item["subshell"] and self._should_expand(results[qid]):
                sub_state = state + "\n" + json.dumps(results[qid], ensure_ascii=False)
                results[f"{qid}_sub"] = item["subshell"].evaluate(sub_state, evaluator)
        return results

    def _should_expand(self, answer: Any) -> bool:
        if isinstance(answer, dict):
            return answer.get("closure", 0) >= 0.7 or answer.get("value", 0) >= 7
        return False


class OpenMonadBuilder:
    """2.2 Open monad — model proposes the second pole."""
    @staticmethod
    def as_questions(pole_a: str, criteria: str) -> Dict[str, Dict]:
        return {
            "propose_pole_b": {
                "type": "choice",
                "options": ["смысл", "содержание", "следствие", "следующий уровень", "другое"],
                "criteria": f"Какой второй полюс естественно дополняет '{pole_a}'. {criteria}"
            },
            "closure": {
                "type": "score",
                "min": 0,
                "max": 10,
                "criteria": f"Насколько устойчиво замыкается отношение. {criteria}"
            },
            "generates_higher": {
                "type": "noul",
                "criteria": "Порождает ли следующий уровень"
            }
        }


class MultiMonadEvaluator:
    """2.3 Multi-monad."""
    def __init__(self, dualities: list):
        self.dualities = dualities

    def build_questions(self) -> Dict[str, Dict]:
        qs = {}
        for d in self.dualities:
            qs[d["id"]] = {
                "type": "monad",
                "pole_a": d["pole_a"],
                "pole_b": d["pole_b"],
                "criteria": d["criteria"]
            }
        qs["overall_coherence"] = {
            "type": "score",
            "min": 0,
            "max": 10,
            "criteria": "Насколько согласованы все двойственности"
        }
        return qs


class TemporalMonad:
    """2.4 Temporal monad."""
    @staticmethod
    def as_questions(pole_a: str, pole_b: str, criteria: str) -> Dict[str, Dict]:
        return {
            "before": {
                "type": "monad",
                "pole_a": pole_a,
                "pole_b": pole_b,
                "criteria": f"Состояние ДО. {criteria}"
            },
            "after": {
                "type": "monad",
                "pole_a": pole_a,
                "pole_b": pole_b,
                "criteria": f"Состояние ПОСЛЕ. {criteria}"
            },
            "direction": {
                "type": "choice",
                "options": ["усилилось", "ослабло", "сменилось доминирование", "без изменений"],
                "criteria": "Как изменилось отношение"
            }
        }


class EvolutionarySelector:
    """3.3 Evolutionary selection of criteria."""
    def __init__(self):
        self.candidates = []

    def add_candidate(self, criteria: str, runs: list):
        mean = statistics.mean(runs) if runs else 0.0
        stdev = statistics.stdev(runs) if len(runs) > 1 else 0.0
        self.candidates.append({
            "criteria": criteria,
            "mean": mean,
            "stdev": stdev,
            "score": mean - stdev
        })

    def best(self, top_k: int = 1):
        return sorted(self.candidates, key=lambda c: c["score"], reverse=True)[:top_k]


class BoundedGrowthCatalog(HierarchicalCatalog):
    """3.4 Structural boundedness."""
    def __init__(self, max_subshells_per_level: int = 3, **kwargs):
        super().__init__(**kwargs)
        self.max_subshells_per_level = max_subshells_per_level
        self.created_per_level = {}

    def can_add_subshell(self, level_id: str) -> bool:
        return self.created_per_level.get(level_id, 0) < self.max_subshells_per_level

    def record_subshell(self, level_id: str):
        self.created_per_level[level_id] = self.created_per_level.get(level_id, 0) + 1


class InvariantSearcher(ReferenceFrameEvaluator):
    """4.2 Invariant search."""
    def find_invariants(self, results: Dict[str, Dict], threshold: float = 0.15):
        all_qids = set()
        for frame_ans in results.values():
            all_qids.update(frame_ans.keys())
        invariants = []
        for qid in all_qids:
            values = []
            for frame_ans in results.values():
                a = frame_ans.get(qid, {})
                if isinstance(a, dict):
                    v = a.get("confidence") or a.get("probability") or (a.get("value", 0) / 10.0)
                    if v is not None:
                        values.append(float(v))
            if len(values) >= 2 and statistics.stdev(values) <= threshold:
                invariants.append(qid)
        return invariants


class AdaptiveFrameEvaluator:
    """4.3 Adaptive frames."""
    def __init__(self, base_questions: Dict, refine_fn: Callable):
        self.base_questions = base_questions
        self.refine_fn = refine_fn

    def evaluate(self, state: str, evaluator: Callable, max_rounds: int = 2) -> Dict:
        questions = dict(self.base_questions)
        history = []
        for _ in range(max_rounds):
            ans = evaluator(state, questions)
            history.append(ans)
            new_q = {}
            for qid, a in ans.items():
                conf = 0.5
                if isinstance(a, dict):
                    conf = a.get("confidence") or a.get("probability") or 0.5
                if conf < 0.6:
                    refined = self.refine_fn(qid, questions.get(qid, {}))
                    if refined:
                        new_q[qid] = refined
            if not new_q:
                break
            questions.update(new_q)
        return {"final": history[-1] if history else {}, "history": history}


class ClosureComposer:
    """5. Closure-driven composition."""
    def __init__(self, threshold: float = 0.78):
        self.threshold = threshold

    def compose(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        monads = []
        others = {}
        for k, v in answers.items():
            if isinstance(v, dict) and v.get("type") == "monad" and v.get("closure", 0) >= self.threshold:
                monads.append((k, v))
            else:
                others[k] = v
        composed = {"atomic": others, "closed_monads": monads}
        if len(monads) >= 2:
            composed["merged"] = {
                "type": "composed_monad",
                "sources": [k for k, _ in monads],
                "avg_closure": statistics.mean(v.get("closure", 0) for _, v in monads)
            }
        return composed


@dataclass
class MultiLevelState:
    """6. Multi-level state."""
    levels: Dict[str, str] = field(default_factory=dict)

    def add(self, level_id: str, text: str):
        self.levels[level_id] = text

    def to_prompt(self, target_levels: Optional[list] = None) -> str:
        items = self.levels.items()
        if target_levels:
            items = [(k, v) for k, v in self.levels.items() if k in target_levels]
        return "\n\n".join(f"[{lid}]\n{text}" for lid, text in items)


class MultiLevelEvaluator:
    def evaluate(self, state: MultiLevelState, questions: Dict, evaluator: Callable) -> Dict:
        results = {}
        for qid, q in questions.items():
            targets = q.get("target_levels")
            prompt = state.to_prompt(targets)
            ans = evaluator(prompt, {qid: q})
            results[qid] = ans.get(qid, ans)
        return results


class DualityCalibrationLog:
    """7. Duality calibration."""
    def __init__(self):
        self.records = []

    def log(self, pole_a: str, pole_b: str, closure: float, generates: bool, confirmed=None):
        self.records.append({
            "pole_a": pole_a,
            "pole_b": pole_b,
            "closure": closure,
            "generates": generates,
            "confirmed": confirmed
        })

    def summary(self) -> Dict[str, Any]:
        if not self.records:
            return {"count": 0}
        closures = [r["closure"] for r in self.records]
        return {
            "count": len(self.records),
            "mean_closure": statistics.mean(closures),
            "high_closure_ratio": sum(1 for c in closures if c >= 0.75) / len(closures),
            "generate_ratio": sum(1 for r in self.records if r["generates"]) / len(self.records)
        }


class HybridOrchestrator:
    """8. Hybrid orchestrator."""
    def __init__(self, catalog, composer=None, generator=None, calibrator=None):
        self.catalog = catalog
        self.composer = composer or ClosureComposer()
        self.generator = generator or GenerativeCatalog()
        self.calibrator = calibrator or DualityCalibrationLog()

    def run(self, state: str, evaluator: Callable) -> Dict[str, Any]:
        level_results = self.catalog.evaluate(state, evaluator)
        composed = {}
        suggestions = []
        for lid, res in level_results.items():
            if hasattr(res, "answers"):
                composed[lid] = self.composer.compose(res.answers)
                for m in getattr(res, "monads", []):
                    self.calibrator.log(m.pole_a, m.pole_b, m.closure, m.generates_higher_level)
                    sug = self.generator.suggest_from_monad(m)
                    if sug:
                        suggestions.append(sug)
            else:
                composed[lid] = res
        return {
            "levels": level_results,
            "composed": composed,
            "suggestions": suggestions,
            "calibration": self.calibrator.summary()
        }
