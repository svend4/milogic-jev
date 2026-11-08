# Уточнение (Refinement) через структуры Крюкова

## Что добавлено

`refinement.py` — слой, который автоматически превращает сильные монады
в маленькие подкаталоги по выбранной структуре (трилистник, три сферы, клевер и т.д.).

## Основные функции

- `monad_to_subcatalog(monad, structure)` — одна монада → готовый HierarchicalCatalog
- `refine_all_strong(level_results, structure)` — все сильные монады → список пакетов
- `RefinementOrchestrator` — запуск базового каталога + автоматическая генерация уточнений

## Пример

```python
from milogic_jev.refinement import RefinementOrchestrator
from milogic_jev.symbolic import SymbolicAdvisor, build_tarot_business_catalog

advisor = SymbolicAdvisor(build_tarot_business_catalog())
orch = RefinementOrchestrator(default_structure="trefoil")

result = orch.run(
    base_catalog=advisor.catalog,
    state="Описание ситуации",
    evaluator=your_jev,
    evaluate_sub=True,
)

for r in result["refinements"]:
    print(r["base"], r["sub_variants"])
```

Это продолжение надстройки: теперь структуры из `data2` не просто описываются,
а сразу порождают рабочие подкаталоги для дальнейшей оценки.
