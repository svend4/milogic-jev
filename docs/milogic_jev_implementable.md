# Реализуемые схемы и примеры новых классов

## 1. Формат монадического вопроса (готовая схема)

### Запрос
```json
{
  "state": "Двойственное отношение: замысел (атом водорода) ↔ смысл (периодическая система). По Беляеву, вкладывая в замысел смысл атома водорода, получаем закон эволюции периодической системы.",
  "questions": {
    "hydrogen_periodic": {
      "type": "monad",
      "pole_a": "замысел (атом водорода)",
      "pole_b": "смысл (периодическая система)",
      "criteria": "Оценить устойчивость и замкнутость этого двойственного отношения по принципам милогии"
    }
  }
}
```

### Ответ
```json
{
  "hydrogen_periodic": {
    "type": "monad",
    "pole_a": "замысел (атом водорода)",
    "pole_b": "смысл (периодическая система)",
    "dominant": "замысел",
    "dominance_probability": 0.71,
    "closure": 0.84,
    "generates_higher_level": true,
    "higher_level_confidence": 0.67,
    "relation_type": "complementary",
    "suggested_next_level": "ядерные оболочки как следующий уровень иерархии"
  }
}
```

## 2. Иерархический каталог (YAML)

```yaml
name: milogic_hierarchy_v1
levels:
  - id: L0_basis
    questions:
      - id: duality_present
        type: noul
        criteria: "В тексте присутствует явная двойственность"
      - id: duality_type
        type: choice
        options: ["замысел-смысл", "форма-содержание", "яйцо-курица", "другое"]
        criteria: "Тип доминирующей двойственности"
  - id: L1_closure
    depends_on: [L0_basis]
    questions:
      - id: closure_strength
        type: score
        min: 0
        max: 10
        criteria: "Насколько сильно двойственность нижнего уровня замкнулась в новую истину"
      - id: is_stable
        type: noul
        criteria: "Замыкание устойчиво и воспроизводимо"
```

## 3. Полный пример каталога для фрагмента милогии

```yaml
catalog_id: belyaev_hierarchy_core
description: Каталог для оценки утверждений о иерархии материи

questions:
  hydrogen_as_basis:
    type: monad
    pole_a: "атом водорода как замысел"
    pole_b: "периодическая система как смысл"
    criteria: "Является ли атом водорода достаточным базисом для порождения периодической системы"

  periodic_closure:
    type: score
    min: 0
    max: 10
    criteria: "Насколько периодическая система является замкнутой оболочкой 2-го уровня иерархии"
    depends_on: [hydrogen_as_basis]

  nuclear_transition:
    type: noul
    criteria: "Ядерные оболочки естественно следуют из периодической системы как следующий уровень"
    depends_on: [periodic_closure]
```

## 4. Что можно реализовать прямо сейчас

| Компонент | Статус | Что нужно |
|-----------|--------|-----------|
| Монада как шаблон | Готово | Только постобработка ответов Jev |
| Иерархический каталог | Готово | Оркестратор из core.py |
| Правило замыкания | Готово | Логика в HierarchicalCatalog |
| Генерация следующего уровня | Готово | GenerativeCatalog |
| Смена системы отсчёта | Готово | ReferenceFrameEvaluator |

Самый практичный путь: использовать классы из `core.py` поверх существующего Jev.
