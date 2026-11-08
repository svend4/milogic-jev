"""
Comprehensive domain and symbolic-system catalogs.

Domains: trade, services, manufacturing, education, healthcare,
         finance, real estate, IT/digital, consulting, personal projects.
Systems: Tarot (Major Arcana), I Ching (selected hexagrams),
         direct business dualities, social dualities.
"""

from typing import Dict, List
from .core import HierarchicalCatalog


DOMAINS: Dict[str, List[Dict]] = {
    "trade": [
        {"id": "supply_demand", "pole_a": "предложение", "pole_b": "спрос", "criteria": "Баланс предложения и спроса"},
        {"id": "price_value", "pole_a": "цена", "pole_b": "ценность", "criteria": "Соответствие цены воспринимаемой ценности"},
        {"id": "channel_direct", "pole_a": "каналы", "pole_b": "прямой контакт", "criteria": "Эффективность каналов vs прямых продаж"},
        {"id": "stock_turnover", "pole_a": "запас", "pole_b": "оборачиваемость", "criteria": "Оптимальный уровень запасов"},
    ],
    "services": [
        {"id": "expertise_delivery", "pole_a": "экспертиза", "pole_b": "доставка результата", "criteria": "Хватает ли экспертизы для обещанного результата"},
        {"id": "client_process", "pole_a": "потребность клиента", "pole_b": "процесс оказания", "criteria": "Совпадает ли процесс с реальной потребностью"},
        {"id": "scale_quality", "pole_a": "масштабирование", "pole_b": "качество", "criteria": "Можно ли расти без падения качества"},
        {"id": "capacity_demand", "pole_a": "мощность", "pole_b": "нагрузка", "criteria": "Соответствие мощности текущей нагрузке"},
    ],
    "manufacturing": [
        {"id": "capacity_demand", "pole_a": "производственная мощность", "pole_b": "спрос", "criteria": "Баланс мощности и спроса"},
        {"id": "quality_cost", "pole_a": "качество", "pole_b": "себестоимость", "criteria": "Оптимальное соотношение качества и затрат"},
        {"id": "flexibility_standard", "pole_a": "гибкость", "pole_b": "стандартизация", "criteria": "Нужна ли адаптация или жёсткий стандарт"},
        {"id": "inventory_flow", "pole_a": "запасы", "pole_b": "поток", "criteria": "Уровень незавершённого производства"},
    ],
    "education": [
        {"id": "content_method", "pole_a": "содержание", "pole_b": "метод передачи", "criteria": "Соответствие содержания способу обучения"},
        {"id": "individual_group", "pole_a": "индивидуальный подход", "pole_b": "групповой формат", "criteria": "Баланс персонализации и масштаба"},
        {"id": "theory_practice", "pole_a": "теория", "pole_b": "практика", "criteria": "Достаточно ли практики для закрепления"},
        {"id": "motivation_structure", "pole_a": "мотивация", "pole_b": "структура программы", "criteria": "Удерживает ли структура мотивацию"},
    ],
    "healthcare": [
        {"id": "prevention_treatment", "pole_a": "профилактика", "pole_b": "лечение", "criteria": "Приоритет профилактики или лечения"},
        {"id": "access_quality", "pole_a": "доступность", "pole_b": "качество", "criteria": "Баланс охвата и глубины помощи"},
        {"id": "protocol_individual", "pole_a": "протокол", "pole_b": "индивидуальный подход", "criteria": "Где можно отступить от стандарта"},
        {"id": "resource_outcome", "pole_a": "ресурсы", "pole_b": "результат", "criteria": "Эффективность использования ресурсов"},
    ],
    "finance": [
        {"id": "risk_return", "pole_a": "риск", "pole_b": "доходность", "criteria": "Соотношение риска и ожидаемой доходности"},
        {"id": "liquidity_growth", "pole_a": "ликвидность", "pole_b": "рост", "criteria": "Баланс доступности средств и инвестирования"},
        {"id": "short_long", "pole_a": "краткосрочные цели", "pole_b": "долгосрочные цели", "criteria": "Приоритет горизонта"},
        {"id": "cost_value", "pole_a": "затраты", "pole_b": "создаваемая ценность", "criteria": "Окупаемость текущих расходов"},
    ],
    "real_estate": [
        {"id": "location_price", "pole_a": "локация", "pole_b": "цена", "criteria": "Соответствие цены локации"},
        {"id": "occupancy_yield", "pole_a": "заполняемость", "pole_b": "доходность", "criteria": "Баланс заполнения и ставки"},
        {"id": "maintenance_appreciation", "pole_a": "содержание", "pole_b": "прирост стоимости", "criteria": "Инвестиции в содержание vs ожидание роста"},
        {"id": "tenant_owner", "pole_a": "арендатор", "pole_b": "собственник", "criteria": "Устойчивость отношений"},
    ],
    "it_digital": [
        {"id": "feature_stability", "pole_a": "новые функции", "pole_b": "стабильность", "criteria": "Можно ли добавлять функции без риска"},
        {"id": "speed_quality", "pole_a": "скорость разработки", "pole_b": "качество", "criteria": "Баланс темпа и надёжности"},
        {"id": "user_tech", "pole_a": "потребность пользователя", "pole_b": "технические ограничения", "criteria": "Соответствие решения реальной задаче"},
        {"id": "scale_cost", "pole_a": "масштабируемость", "pole_b": "стоимость", "criteria": "Оптимальный уровень масштабирования"},
    ],
    "consulting": [
        {"id": "diagnosis_action", "pole_a": "диагностика", "pole_b": "действие", "criteria": "Достаточно ли анализа для рекомендаций"},
        {"id": "expertise_implementation", "pole_a": "экспертиза", "pole_b": "внедрение", "criteria": "Готовность клиента к реализации"},
        {"id": "scope_depth", "pole_a": "широта охвата", "pole_b": "глубина", "criteria": "Где нужен фокус"},
        {"id": "independence_dependence", "pole_a": "автономия клиента", "pole_b": "зависимость от консультанта", "criteria": "Формируется ли самостоятельность"},
    ],
    "personal_project": [
        {"id": "vision_resources", "pole_a": "видение", "pole_b": "ресурсы", "criteria": "Соответствие замысла доступным ресурсам"},
        {"id": "action_reflection", "pole_a": "действие", "pole_b": "осмысление", "criteria": "Нужна ли пауза или продолжение"},
        {"id": "solo_collaboration", "pole_a": "самостоятельно", "pole_b": "с партнёрами", "criteria": "Где нужна помощь"},
        {"id": "short_long", "pole_a": "ближайший шаг", "pole_b": "долгая цель", "criteria": "Связь текущего действия с целью"},
    ],
}


def build_domain_catalog(domain: str, max_levels: int = 2) -> HierarchicalCatalog:
    if domain not in DOMAINS:
        raise ValueError(f"Unknown domain: {domain}. Available: {list(DOMAINS.keys())}")
    dualities = DOMAINS[domain]
    cat = HierarchicalCatalog(max_levels=max_levels, closure_threshold=0.72)
    questions = {
        d["id"]: {"type": "monad", "pole_a": d["pole_a"], "pole_b": d["pole_b"], "criteria": d["criteria"]}
        for d in dualities
    }
    cat.add_level("L0", questions, description=f"Двойственности: {domain}")
    cat.add_level(
        "L1",
        questions={
            "priority_action": {
                "type": "choice",
                "options": ["усилить слабый полюс", "зафиксировать сильный", "пересмотреть модель", "подождать", "перейти на следующий уровень"],
                "criteria": "Какое действие приоритетно по итогам оценки",
            }
        },
        condition=lambda ctx: True,
        description="Приоритетное действие",
    )
    return cat


def list_domains() -> List[str]:
    return list(DOMAINS.keys())


I_CHING_HEXAGRAMS = [
    {"id": "1_qian", "name": "Творчество (Цянь)", "pole_a": "инициатива", "pole_b": "устойчивость", "criteria": "Хватает ли силы начинания для длительного движения"},
    {"id": "2_kun", "name": "Исполнение (Кунь)", "pole_a": "принятие", "pole_b": "структурирование", "criteria": "Можно ли принять текущее и придать ему форму"},
    {"id": "11_tai", "name": "Расцвет (Тай)", "pole_a": "гармония", "pole_b": "рост", "criteria": "Устойчив ли текущий баланс для дальнейшего роста"},
    {"id": "12_pi", "name": "Упадок (Пи)", "pole_a": "застой", "pole_b": "необходимость изменения", "criteria": "Требует ли ситуация качественного сдвига"},
    {"id": "24_fu", "name": "Возвращение (Фу)", "pole_a": "возврат к основам", "pole_b": "новый цикл", "criteria": "Пора ли вернуться к простому и начать заново"},
    {"id": "46_sheng", "name": "Подъём (Шэн)", "pole_a": "постепенный рост", "pole_b": "ускорение", "criteria": "Можно ли ускоряться без потери основания"},
    {"id": "47_kun", "name": "Истощение (Кунь)", "pole_a": "ограничение ресурсов", "pole_b": "поиск выхода", "criteria": "Есть ли путь при текущих ограничениях"},
    {"id": "63_jiji", "name": "Уже конец (Цзи Цзи)", "pole_a": "завершение", "pole_b": "поддержание", "criteria": "Замкнут ли цикл и что нужно для его сохранения"},
]


def build_iching_catalog(max_hex: int = 4) -> HierarchicalCatalog:
    cat = HierarchicalCatalog(max_levels=2, closure_threshold=0.74)
    questions = {}
    for h in I_CHING_HEXAGRAMS[:max_hex]:
        questions[h["id"]] = {"type": "monad", "pole_a": h["pole_a"], "pole_b": h["pole_b"], "criteria": h["criteria"]}
    cat.add_level("L0", questions, description="Гексаграммы как двойственности")
    cat.add_level(
        "L1",
        questions={
            "movement": {
                "type": "choice",
                "options": ["продолжать", "скорректировать", "остановиться", "сменить уровень"],
                "criteria": "Какое движение следует из оценки",
            }
        },
        condition=lambda ctx: True,
    )
    return cat


SOCIAL_DUALITIES = [
    {"id": "individual_collective", "pole_a": "индивидуальное", "pole_b": "коллективное", "criteria": "Баланс личной инициативы и общих правил"},
    {"id": "formal_informal", "pole_a": "формальные процессы", "pole_b": "неформальные связи", "criteria": "Где работают правила, а где — отношения"},
    {"id": "stability_change", "pole_a": "стабильность", "pole_b": "изменения", "criteria": "Готовность системы к изменению"},
    {"id": "center_periphery", "pole_a": "центр", "pole_b": "периферия", "criteria": "Распределение влияния и ресурсов"},
]


def build_social_catalog() -> HierarchicalCatalog:
    cat = HierarchicalCatalog(max_levels=2, closure_threshold=0.70)
    questions = {
        d["id"]: {"type": "monad", "pole_a": d["pole_a"], "pole_b": d["pole_b"], "criteria": d["criteria"]}
        for d in SOCIAL_DUALITIES
    }
    cat.add_level("L0", questions, description="Социальные и организационные двойственности")
    cat.add_level(
        "L1",
        questions={
            "intervention": {
                "type": "choice",
                "options": ["усилить слабую сторону", "закрепить сильную", "пересмотреть структуру", "наблюдать"],
                "criteria": "Какое вмешательство целесообразно",
            }
        },
        condition=lambda ctx: True,
    )
    return cat


def get_all_catalog_builders() -> Dict[str, callable]:
    builders = {f"domain_{name}": (lambda n=name: build_domain_catalog(n)) for name in DOMAINS}
    builders["iching"] = build_iching_catalog
    builders["social"] = build_social_catalog
    return builders
