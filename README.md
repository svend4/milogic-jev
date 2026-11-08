# Milogic-Jev

Иерархические системы принятия решений, сочетающие:

- типизированные вопросы и калибровку (принцип Jev),
- двойственные отношения, замыкание и «образ и подобие» (милогия Беляева),
- структуры уточнения (Крюков / data2),
- носители с двумя режимами и zero (alice-snov).

## Слои

| Слой | Модуль | Назначение |
|------|--------|------------|
| Ядро | `core.py` | Монады, HierarchicalCatalog, замыкание |
| Варианты | `variants.py` | 8+ классов и подвидов |
| Домены | `catalogs_extended.py` | 10 сфер (trade, services, finance…) |
| Символика | `symbolic.py` | Таро как бизнес-монады |
| Kryukov | `kryukov_extension.py` | trefoil, three_spheres, clover… |
| Refinement | `refinement.py` | Автогенерация подкаталогов |
| Микро-архетипы | `micro_archetypes.py` | Шестерёнки + игровые сцены |
| Носители | `carriers.py` | 12 носителей alice-snov |
| Сцены носителей | `carrier_scenes.py` | Сцены с явным zero |
| Пайплайн | `pipeline.py` | Единый вход |

## Быстрый старт

```python
from milogic_jev import (
    build_domain_catalog,
    SymbolicAdvisor,
    MicroArchetypeLayer,
    build_carrier_catalog,
    CarrierSceneLayer,
)

# Домен + микро-архетипы
cat = build_domain_catalog("services")
advisor = SymbolicAdvisor(cat)
results = advisor.catalog.evaluate(state, your_evaluator)

layer = MicroArchetypeLayer(max_gears=3)
for item in layer.enrich(results):
    print(item["monad"])
    print(item["scene"]["scene"])

# Носители alice-snov
carrier_cat = build_carrier_catalog(max_carriers=6)
c_advisor = SymbolicAdvisor(carrier_cat)
c_results = c_advisor.catalog.evaluate(state, your_evaluator)

scenes = CarrierSceneLayer().enrich(c_results)
for s in scenes:
    print(s["scene"])
```

## Пайплайн

```python
from milogic_jev import run_domain_with_refinement

result = run_domain_with_refinement(
    domain="services",
    state="Спрос растёт, процессы не успевают",
    evaluator=your_evaluator,
    structure="three_spheres",
    evaluate_sub=True,
)
print(result["summary"])
```

## Документация

- `docs/CATALOGS.md` — домены
- `docs/KRYUKOV_EXTENSION.md` — структуры
- `docs/REFINEMENT.md` — подкаталоги
- `docs/MICRO_ARCHETYPES.md` — шестерёнки
- `docs/CARRIERS.md` — носители
- `docs/PIPELINE.md` — единый вход

## Демо

```bash
python -m milogic_jev.demo_catalogs
python -m milogic_jev.demo_micro
python -m milogic_jev.demo_carriers
python -m milogic_jev.demo_pipeline
```

## Источники

- Милогия М.И. Беляева
- Jev (TypeSafe AI)
- data2 / Крюков
- [alice-snov](https://github.com/svend4/alice-snov)
