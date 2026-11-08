# Пайплайн: домен → монады → структура Крюкова

## Назначение

Единый вход, который связывает:

1. Доменный каталог (`trade`, `services`, …)
2. Оценку базовых монад
3. Автоматическое разворачивание сильных монад в структуру из `data2`
   (trefoil, three_spheres, clover и т.д.)

## Функции

- `run_domain_with_refinement(domain, state, evaluator, structure)`
- `DomainPipeline(domain, structure)` — обёртка с фиксированным доменом
- `available_structures()` — список доступных структур

## Пример

```python
from milogic_jev.pipeline import run_domain_with_refinement

result = run_domain_with_refinement(
    domain="services",
    state="Спрос растёт, процессы не успевают",
    evaluator=your_jev,
    structure="three_spheres",
    evaluate_sub=True,
)

print(result["summary"])
for r in result["refinements"]:
    print(r["base"], r["sub_variants"])
```

Это замыкает цепочку: доменный каталог + слой уточнения из структур Крюкова.
