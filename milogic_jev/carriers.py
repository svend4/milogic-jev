"""Carrier catalog from alice-snov (Physics of Carriers)."""

from typing import Dict, List
from .core import HierarchicalCatalog


CARRIERS: List[Dict] = [
    {"id": "ski_rocker", "name": "Кресло-лыжи", "geometry": "кривая", "mode_a": "осцилляция", "mode_b": "трансляция", "zero": "снятые ботинки", "apparatus": "rocker-rail", "criteria": "Один рельс на колебание и перемещение"},
    {"id": "phase_wheel", "name": "Вело-часы", "geometry": "круг + цепь", "mode_a": "катить", "mode_b": "тикать", "zero": "снятая цепь", "apparatus": "phase-lock wheel", "criteria": "Цепь связывает два режима на одном колесе"},
    {"id": "opcode_dial", "name": "Часы-приборы", "geometry": "вал", "mode_a": "резать", "mode_b": "черпать", "zero": "пустой циферблат", "apparatus": "opcode-bus", "criteria": "Две операции на одном такте"},
    {"id": "chandelier", "name": "Люстра-фонтан", "geometry": "рожок", "mode_a": "светить", "mode_b": "стекать", "zero": "потухший фитиль", "apparatus": "hold+drain bus", "criteria": "Свет и сток на одном объёме"},
    {"id": "ship_needle", "name": "Корабль в игле", "geometry": "сечение", "mode_a": "остаться", "mode_b": "пройти", "zero": "закрытая пробоина", "apparatus": "hostile aperture", "criteria": "Один объект — два пропуска"},
    {"id": "book_stairs", "name": "Лестница-книги", "geometry": "ступень", "mode_a": "идти", "mode_b": "миновать ряд", "zero": "закрытая книга", "apparatus": "index stair", "criteria": "Шаг или пропуск на одной ступени"},
    {"id": "tray_face", "name": "Поднос-лицо", "geometry": "плоскость", "mode_a": "собрать", "mode_b": "быть лицом", "zero": "пустой поднос", "apparatus": "synthesis platen", "criteria": "Части складываются в лицо"},
    {"id": "hat", "name": "Шляпа", "geometry": "цилиндр", "mode_a": "надеть", "mode_b": "разложить", "zero": "пустой цилиндр", "apparatus": "decomposition volume", "criteria": "Одно надевание — четыре квадрата"},
    {"id": "snowflake", "name": "Снежинка", "geometry": "дендрит", "mode_a": "вверх", "mode_b": "падение", "zero": "молчание", "apparatus": "vector inverter", "criteria": "Направление инвертируется без рукопожатия"},
    {"id": "white_friend", "name": "Белый друг", "geometry": "порог", "mode_a": "неверная дверь", "mode_b": "карта", "zero": "закрытый порог", "apparatus": "wrong-door as map", "criteria": "Ошибка становится ориентиром"},
    {"id": "assol", "name": "Ассоль", "geometry": "берег", "mode_a": "ждать", "mode_b": "остановить", "zero": "пустой берег", "apparatus": "dead-quest detector", "criteria": "Остановка вместо повтора"},
    {"id": "honest_bus", "name": "Уходит Бог", "geometry": "шина", "mode_a": "один канал", "mode_b": "отбросить остальные", "zero": "молчание шины", "apparatus": "honest-bus filter", "criteria": "Одна физическая линия"},
]


def build_carrier_catalog(max_carriers: int = 6) -> HierarchicalCatalog:
    cat = HierarchicalCatalog(max_levels=2, closure_threshold=0.72)
    questions = {}
    for c in CARRIERS[:max_carriers]:
        questions[c["id"]] = {
            "type": "monad",
            "pole_a": c["mode_a"],
            "pole_b": c["mode_b"],
            "criteria": c["criteria"],
            "geometry": c["geometry"],
            "zero": c["zero"],
            "apparatus": c["apparatus"],
        }
    cat.add_level("L0_carriers", questions, description="Носители: один объект — два режима")
    cat.add_level(
        "L1_zero",
        questions={
            "zero_state": {
                "type": "choice",
                "options": ["назвать zero", "отклонить 100% A", "отклонить 100% B", "перенести на новый объект"],
                "criteria": "Что делать с точкой zero",
            }
        },
        condition=lambda ctx: True,
        description="Работа с zero",
    )
    return cat


def list_carriers() -> List[str]:
    return [c["id"] for c in CARRIERS]


def get_carrier(carrier_id: str) -> Dict:
    for c in CARRIERS:
        if c["id"] == carrier_id:
            return c
    raise KeyError(carrier_id)
