# Микро-архетипы («шестерёнки») и игровой слой

## Идея

Поверх сильной монады (карты / двойственности) накладываются короткие именованные циклы — «шестерёнки» ситуации.
Логика расчёта не меняется. Меняется только детализация и форма выдачи.

## Микро-архетипы

| id | Название | Размер | Игровой объект |
|----|----------|--------|----------------|
| check | Проверка | малый | маленькая шестерёнка |
| launch | Запуск | средний | средняя шестерёнка |
| fix | Закрепление | средний | стопорная шестерёнка |
| shift | Сдвиг | большой | большая шестерёнка с рычагом |
| observe | Наблюдение | малый | прозрачная линза |

## Использование

```python
from milogic_jev.micro_archetypes import MicroArchetypeLayer
from milogic_jev.symbolic import SymbolicAdvisor, build_tarot_business_catalog

advisor = SymbolicAdvisor(build_tarot_business_catalog())
results = advisor.catalog.evaluate(state, evaluator)

layer = MicroArchetypeLayer(max_gears=3)
enriched = layer.enrich(results)

for item in enriched:
    print(item["monad"])
    print(item["scene"]["scene"])
    for g in item["gears"]:
        print(g["name"], g["game_object"])
```

Это слой представления и мелкой детализации.  
Он совместим с доменными каталогами, refinement и пайплайном.
