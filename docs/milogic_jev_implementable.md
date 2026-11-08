# Реализуемые схемы и примеры новых классов

## 1. Формат монадического вопроса

### Запрос
```json
{
  "state": "Двойственное отношение: замысел (атом водорода) ↔ смысл (периодическая система).",
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
    "suggested_next_level": "ядерные оболочки"
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
  - id: L1_closure
    depends_on: [L0_basis]
    questions:
      - id: closure_strength
        type: score
        min: 0
        max: 10
        criteria: "Сила замыкания двойственности нижнего уровня"
```

## 3. Пример каталога под фрагмент милогии

```yaml
catalog_id: belyaev_hierarchy_core
questions:
  hydrogen_as_basis:
    type: monad
    pole_a: "атом водорода как замысел"
    pole_b: "периодическая система как смысл"
  periodic_closure:
    type: score
    min: 0
    max: 10
    criteria: "Насколько периодическая система является замкнутой оболочкой 2-го уровня"
    depends_on: [hydrogen_as_basis]
```

Полные схемы, псевдокод и примеры Python-структур см. в локальном файле milogic_jev_implementable.md (можно добавить при необходимости).
