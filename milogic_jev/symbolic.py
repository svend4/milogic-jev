"""
Tarot and symbolic systems as hierarchical dual-relation catalogs
for recommendation and project management (Lebensberater / entrepreneurship).

Not divination — structured monads + Jev-style evaluation.
"""

from typing import Dict, Any, Optional
from .core import HierarchicalCatalog, GenerativeCatalog


MAJOR_ARCANA_BUSINESS = [
    {"id": "magician", "name": "Маг", "pole_a": "ресурсы и инструменты", "pole_b": "реализация и действие", "criteria": "Насколько доступные ресурсы уже готовы к конкретному действию"},
    {"id": "high_priestess", "name": "Жрица", "pole_a": "явная информация", "pole_b": "скрытые факторы и интуиция", "criteria": "Достаточно ли явных данных или нужно учесть скрытое"},
    {"id": "empress", "name": "Императрица", "pole_a": "рост и плодородие", "pole_b": "удержание и структура", "criteria": "Можно ли масштабировать без потери устойчивости"},
    {"id": "emperor", "name": "Император", "pole_a": "контроль и порядок", "pole_b": "гибкость и адаптация", "criteria": "Где сейчас нужен жёсткий каркас, а где — свобода"},
    {"id": "hierophant", "name": "Иерофант", "pole_a": "проверенные практики", "pole_b": "новые подходы", "criteria": "Следовать ли существующим правилам или менять модель"},
    {"id": "lovers", "name": "Влюблённые", "pole_a": "партнёрство и выбор", "pole_b": "автономия и собственный путь", "criteria": "Усиливает ли текущее сотрудничество или ограничивает"},
    {"id": "chariot", "name": "Колесница", "pole_a": "движение и скорость", "pole_b": "направление и контроль", "criteria": "Есть ли ясный вектор при высокой скорости"},
    {"id": "strength", "name": "Сила", "pole_a": "внутренний ресурс", "pole_b": "внешнее давление", "criteria": "Хватает ли внутренней устойчивости под нагрузкой"},
    {"id": "hermit", "name": "Отшельник", "pole_a": "анализ и пауза", "pole_b": "действие и коммуникация", "criteria": "Нужна ли сейчас пауза для ясности или пора выходить"},
    {"id": "wheel", "name": "Колесо Фортуны", "pole_a": "внешние циклы", "pole_b": "управляемые факторы", "criteria": "Что можно контролировать, а что является циклом среды"},
    {"id": "justice", "name": "Справедливость", "pole_a": "баланс и договорённости", "pole_b": "дисбаланс и претензии", "criteria": "Насколько текущие договорённости устойчивы"},
    {"id": "hanged", "name": "Повешенный", "pole_a": "текущая модель", "pole_b": "смена точки зрения", "criteria": "Даёт ли смена перспективы новое замыкание"},
    {"id": "death", "name": "Смерть", "pole_a": "завершение старого", "pole_b": "рождение нового", "criteria": "Готов ли процесс к качественному переходу"},
    {"id": "temperance", "name": "Умеренность", "pole_a": "смешение и синтез", "pole_b": "чистота подхода", "criteria": "Нужна ли интеграция разных элементов или фокус"},
    {"id": "devil", "name": "Дьявол", "pole_a": "зависимость и ограничение", "pole_b": "осознанный выход", "criteria": "Есть ли скрытые привязки, которые блокируют развитие"},
    {"id": "tower", "name": "Башня", "pole_a": "внезапное разрушение", "pole_b": "освобождение структуры", "criteria": "Является ли текущий кризис очищением или просто потерей"},
    {"id": "star", "name": "Звезда", "pole_a": "видение и надежда", "pole_b": "конкретные шаги", "criteria": "Есть ли достаточно ясный образ будущего для движения"},
    {"id": "moon", "name": "Луна", "pole_a": "неопределённость", "pole_b": "ориентиры", "criteria": "Насколько можно действовать при текущей неясности"},
    {"id": "sun", "name": "Солнце", "pole_a": "ясность и успех", "pole_b": "перегрев и самоуверенность", "criteria": "Устойчив ли текущий успех или он хрупок"},
    {"id": "judgement", "name": "Суд", "pole_a": "оценка прошлого", "pole_b": "призыв к новому циклу", "criteria": "Пора ли подводить итог и начинать следующий уровень"},
    {"id": "world", "name": "Мир", "pole_a": "завершение цикла", "pole_b": "новый уровень", "criteria": "Замкнулся ли текущий цикл и готов ли следующий"},
]


def build_tarot_business_catalog(max_cards: int = 3) -> HierarchicalCatalog:
    cat = HierarchicalCatalog(max_levels=3, closure_threshold=0.75)
    l0_questions = {}
    for card in MAJOR_ARCANA_BUSINESS[:max_cards]:
        l0_questions[card["id"]] = {
            "type": "monad",
            "pole_a": card["pole_a"],
            "pole_b": card["pole_b"],
            "criteria": card["criteria"]
        }
    cat.add_level("L0_situation", l0_questions, description="Текущая двойственность ситуации")
    cat.add_level(
        "L1_readiness",
        questions={
            "action_readiness": {"type": "score", "min": 0, "max": 10, "criteria": "Готовность к следующему шагу"},
            "risk_of_inaction": {"type": "noul", "criteria": "Риск бездействия выше риска действия"}
        },
        condition=lambda ctx: True,
        description="Готовность к действию"
    )
    cat.add_level(
        "L2_next",
        questions={
            "next_level_viable": {"type": "noul", "criteria": "Есть ли естественный следующий уровень"}
        },
        condition=lambda ctx: True,
        description="Возможность следующего уровня"
    )
    return cat


def recommend_from_results(level_results: Dict) -> Dict[str, Any]:
    rec = {
        "summary": "",
        "dominant_duality": None,
        "closure": 0.0,
        "action": "наблюдать",
        "next_step": None,
        "confidence": 0.5
    }
    l0 = level_results.get("L0_situation") or level_results.get("L0")
    if l0 and hasattr(l0, "monads") and l0.monads:
        best = max(l0.monads, key=lambda m: m.closure)
        rec["dominant_duality"] = f"{best.pole_a} ↔ {best.pole_b}"
        rec["closure"] = best.closure
        rec["confidence"] = best.dominance_probability
        if best.is_strongly_closed(0.75):
            rec["action"] = "действовать"
            rec["next_step"] = best.suggested_next_level or "уточнить и зафиксировать следующий шаг"
        elif best.closure >= 0.55:
            rec["action"] = "уточнять"
            rec["next_step"] = "собрать недостающие данные по слабому полюсу"
        else:
            rec["action"] = "пауза"
            rec["next_step"] = "пересмотреть формулировку ситуации"
    rec["summary"] = (
        f"Доминирует: {rec['dominant_duality'] or 'не определено'}. "
        f"Замыкание {rec['closure']:.2f}. Рекомендация: {rec['action']}."
    )
    return rec


TRADE_CATALOG_DUALITIES = [
    {"id": "supply_demand", "pole_a": "предложение", "pole_b": "спрос", "criteria": "Баланс предложения и спроса"},
    {"id": "price_value", "pole_a": "цена", "pole_b": "ценность", "criteria": "Соответствие цены воспринимаемой ценности"},
    {"id": "channel_direct", "pole_a": "каналы", "pole_b": "прямой контакт", "criteria": "Эффективность каналов vs прямых продаж"},
]

SERVICE_CATALOG_DUALITIES = [
    {"id": "expertise_delivery", "pole_a": "экспертиза", "pole_b": "доставка результата", "criteria": "Хватает ли экспертизы для обещанного результата"},
    {"id": "client_process", "pole_a": "потребность клиента", "pole_b": "процесс оказания", "criteria": "Совпадает ли процесс с реальной потребностью"},
    {"id": "scale_quality", "pole_a": "масштабирование", "pole_b": "качество", "criteria": "Можно ли расти без падения качества"},
]


def build_domain_catalog(domain: str = "trade") -> HierarchicalCatalog:
    dualities = TRADE_CATALOG_DUALITIES if domain == "trade" else SERVICE_CATALOG_DUALITIES
    cat = HierarchicalCatalog(max_levels=2, closure_threshold=0.72)
    questions = {
        d["id"]: {"type": "monad", "pole_a": d["pole_a"], "pole_b": d["pole_b"], "criteria": d["criteria"]}
        for d in dualities
    }
    cat.add_level("L0", questions, description=f"Двойственности домена: {domain}")
    cat.add_level(
        "L1",
        questions={
            "priority_action": {
                "type": "choice",
                "options": ["усилить слабый полюс", "зафиксировать сильный", "пересмотреть модель", "подождать"],
                "criteria": "Какое действие приоритетно"
            }
        },
        condition=lambda ctx: True
    )
    return cat


class SymbolicAdvisor:
    """High-level interface: symbolic catalog + evaluator → recommendation."""
    def __init__(self, catalog: HierarchicalCatalog, generator: Optional[GenerativeCatalog] = None):
        self.catalog = catalog
        self.generator = generator or GenerativeCatalog()

    def advise(self, state: str, evaluator) -> Dict[str, Any]:
        results = self.catalog.evaluate(state, evaluator)
        rec = recommend_from_results(results)
        suggestions = []
        for level_res in results.values():
            if hasattr(level_res, "monads"):
                for m in level_res.monads:
                    sug = self.generator.suggest_from_monad(m)
                    if sug:
                        suggestions.append(sug)
        rec["suggestions"] = suggestions
        rec["raw_levels"] = {k: (v.reason if hasattr(v, "reason") else str(v)) for k, v in results.items()}
        return rec
