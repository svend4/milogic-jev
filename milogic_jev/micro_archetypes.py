"""Micro-archetypes ("gears") and game-style presentation layer."""

from typing import Dict, List, Any, Optional
from .core import MonadAnswer


MICRO_ARCHETYPES = {
    "check": {"name": "Проверка", "size": "малый", "description": "Быстрый цикл: проверить текущее состояние полюса", "game_object": "маленькая шестерёнка"},
    "launch": {"name": "Запуск", "size": "средний", "description": "Основной цикл: запустить или усилить доминирующий полюс", "game_object": "средняя шестерёнка"},
    "fix": {"name": "Закрепление", "size": "средний", "description": "Цикл фиксации результата, чтобы не откатиться", "game_object": "стопорная шестерёнка"},
    "shift": {"name": "Сдвиг", "size": "большой", "description": "Переход на следующий уровень или смена доминирования", "game_object": "большая шестерёнка с рычагом"},
    "observe": {"name": "Наблюдение", "size": "малый", "description": "Пауза: смотреть, не действуя", "game_object": "прозрачная линза"},
}


def attach_micro_archetypes(monad: MonadAnswer, max_gears: int = 3) -> List[Dict[str, Any]]:
    order = ["check", "launch", "fix", "shift", "observe"]
    selected = order[:max_gears]
    gears = []
    for key in selected:
        m = MICRO_ARCHETYPES[key]
        gears.append({
            "id": key,
            "name": m["name"],
            "size": m["size"],
            "description": m["description"],
            "game_object": m["game_object"],
            "focus": f"{m['name']}: {monad.dominant or monad.pole_a}",
        })
    return gears


def to_game_scene(monad: MonadAnswer, gears: List[Dict[str, Any]]) -> Dict[str, Any]:
    dominant = monad.dominant or monad.pole_a
    weak = monad.pole_b if dominant == monad.pole_a else monad.pole_a
    return {
        "scene": f"На столе лежит карта «{monad.pole_a} ↔ {monad.pole_b}».",
        "character": f"Фигура, стоящая ближе к «{dominant}».",
        "tension": f"Слабая сторона — «{weak}» (замыкание {monad.closure:.2f}).",
        "gears": [{"object": g["game_object"], "action": g["name"], "hint": g["focus"]} for g in gears],
        "next_move": "Можно крутить любую шестерёнку или подождать.",
    }


class MicroArchetypeLayer:
    """Adds named micro-archetypes and optional game-style scenes."""
    def __init__(self, max_gears: int = 3):
        self.max_gears = max_gears

    def enrich(self, level_results: Dict) -> List[Dict[str, Any]]:
        enriched = []
        for level_name, level_res in level_results.items():
            if not hasattr(level_res, "monads"):
                continue
            for monad in level_res.monads:
                if not monad.is_strongly_closed(0.60):
                    continue
                gears = attach_micro_archetypes(monad, self.max_gears)
                scene = to_game_scene(monad, gears)
                enriched.append({
                    "level": level_name,
                    "monad": f"{monad.pole_a} ↔ {monad.pole_b}",
                    "closure": monad.closure,
                    "gears": gears,
                    "scene": scene,
                })
        return enriched
