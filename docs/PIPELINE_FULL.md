# Расширенный пайплайн

## Функция

`run_full()` объединяет:

- доменный каталог или носители alice-snov,
- refinement (Kryukov-структура),
- микро-архетипы,
- сцены носителей (если `carrier_mode=True`).

## Пример

```python
from milogic_jev.pipeline_full import run_full

# Домен
res = run_full(
    domain="services",
    state="...",
    evaluator=your_jev,
    structure="three_spheres",
    with_micro=True,
)
print(res["summary"])
print(res["micro"][0]["scene"])

# Носители
res2 = run_full(
    carrier_mode=True,
    state="...",
    evaluator=your_jev,
    with_micro=True,
)
print(res2["carrier_scenes"][0]["scene"])
```

## Поля результата

- `summary` — краткая сводка
- `refinements` — подкаталоги от refinement
- `micro` — шестерёнки и сцены
- `carrier_scenes` — сцены носителей (только в carrier_mode)
