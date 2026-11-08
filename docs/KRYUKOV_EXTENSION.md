# Надстройка Kryukov / data2 поверх Milogic-Jev

## Идея

Базовая двойственность (монада) — это фундамент.  
Для более тонкой детализации поверх неё накладываются структуры из репозитория `data2` (по мотивам Крюкова):

- петля / круг
- восьмёрка и деформированная восьмёрка
- трилистник (три лепестка разного размера)
- три сферы (МВС / СВС / БВС)
- клевер / квадрат (4 лепестка)
- 4×4 = 16 состояний
- букет — набор циклов разного размера и «цвета»

Это не замена монад, а **слой уточнения** для сильных замыканий.

## Использование

```python
from milogic_jev.kryukov_extension import StructureExpander
from milogic_jev.symbolic import SymbolicAdvisor, build_tarot_business_catalog

advisor = SymbolicAdvisor(build_tarot_business_catalog())
results = advisor.catalog.evaluate(state, evaluator)

expander = StructureExpander(default_structure="trefoil")
refinements = expander.expand_results(results)

for r in refinements:
    print(r["base_monad"], "→", r["structure"])
    for v in r["sub_variants"]:
        print(" ", v)
```

## Когда какую структуру брать

| Замыкание | Рекомендуемые структуры |
|-----------|-------------------------|
| ≥ 0.85    | clover, four_windows, bouquet |
| ≥ 0.75    | trefoil, three_spheres, figure8 |
| ≥ 0.60    | figure8, loop |
| ниже      | duality (базовая) |

Источник структур: репозиторий [svend4/data2](https://github.com/svend4/data2) (архетипы движения по Крюкову).
