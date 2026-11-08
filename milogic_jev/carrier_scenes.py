"""Alice-snov style presentation layer."""

from typing import Dict, List, Any
from .core import MonadAnswer
from .carriers import get_carrier, CARRIERS


def carrier_to_scene(monad: MonadAnswer, carrier_id: str = None) -> Dict[str, Any]:
    c = None
    if carrier_id:
        try:
            c = get_carrier(carrier_id)
        except KeyError:
            c = None
    if c is None:
        for cand in CARRIERS:
            if cand["mode_a"] == monad.pole_a and cand["mode_b"] == monad.pole_b:
                c = cand
                break
    if c is None:
        c = {"name": "носитель", "geometry": "?", "zero": "не назван", "apparatus": "не назван"}

    dominant = monad.dominant or monad.pole_a
    weak = monad.pole_b if dominant == monad.pole_a else monad.pole_a

    return {
        "object": c["name"],
        "geometry": c.get("geometry", "?"),
        "mode_a": monad.pole_a,
        "mode_b": monad.pole_b,
        "dominant": dominant,
        "weak": weak,
        "zero": c.get("zero", "не назван"),
        "apparatus": c.get("apparatus", "не назван"),
        "closure": monad.closure,
        "law": "50+50=100 внутри объекта",
        "scene": (
            f"Объект «{c['name']}» ({c.get('geometry', '?')}). "
            f"Режим A: {monad.pole_a}. Режим B: {monad.pole_b}. "
            f"Сейчас ближе к «{dominant}». "
            f"Zero: {c.get('zero', '—')}."
        ),
        "next": "Назвать zero или перенести на новый носитель той же геометрии.",
    }


class CarrierSceneLayer:
    """Enrich carrier catalog results with alice-snov style scenes."""
    def enrich(self, level_results: Dict) -> List[Dict[str, Any]]:
        scenes = []
        for level_name, level_res in level_results.items():
            if not hasattr(level_res, "monads"):
                continue
            for monad in level_res.monads:
                if not monad.is_strongly_closed(0.60):
                    continue
                scene = carrier_to_scene(monad)
                scene["level"] = level_name
                scenes.append(scene)
        return scenes
