"""Scene prompts for image generation."""

from typing import Dict, Any, List
from .core import MonadAnswer


def monad_to_prompt(monad: MonadAnswer, style: str = "surreal technical") -> str:
    dominant = monad.dominant or monad.pole_a
    weak = monad.pole_b if dominant == monad.pole_a else monad.pole_a
    return (
        f"{style}, symbolic object representing '{monad.pole_a}' and '{monad.pole_b}', "
        f"emphasis on '{dominant}', weaker presence of '{weak}', "
        f"closure strength {monad.closure:.2f}, "
        "soft lighting, precise geometry, no text"
    )


def micro_to_prompt(gear: Dict[str, Any], base_prompt: str) -> str:
    return (
        f"{base_prompt}, small mechanical element: {gear.get('game_object', 'gear')}, "
        f"labeled conceptually as '{gear.get('name', 'cycle')}'"
    )


def carrier_to_prompt(scene: Dict[str, Any]) -> str:
    return (
        f"surreal technical object '{scene.get('object', 'carrier')}', "
        f"geometry: {scene.get('geometry', 'unknown')}, "
        f"two modes visible: '{scene.get('mode_a')}' and '{scene.get('mode_b')}', "
        f"zero point suggested: {scene.get('zero', 'empty')}, "
        f"apparatus: {scene.get('apparatus', 'unknown')}, "
        "precise, quiet, no text, soft directional light"
    )


def prompts_from_micro(items: List[Dict[str, Any]]) -> List[str]:
    out = []
    for item in items:
        poles = item["monad"].split(" ↔ ")
        if len(poles) != 2:
            continue
        fake = MonadAnswer(
            pole_a=poles[0], pole_b=poles[1],
            dominant=poles[0],
            dominance_probability=0.7,
            closure=item.get("closure", 0.7),
            generates_higher_level=True,
            higher_level_confidence=0.6,
            relation_type="complementary",
            suggested_next_level="",
        )
        base = monad_to_prompt(fake)
        for gear in item.get("gears", [])[:1]:
            out.append(micro_to_prompt(gear, base))
    return out


def prompts_from_carriers(scenes: List[Dict[str, Any]]) -> List[str]:
    return [carrier_to_prompt(s) for s in scenes]
