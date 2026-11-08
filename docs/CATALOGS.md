# Расширенные каталоги: сферы и системы

## Домены

| Домен | Ключевые двойственности |
|-------|-------------------------|
| trade | предложение↔спрос, цена↔ценность, каналы↔прямой контакт |
| services | экспертиза↔доставка, потребность↔процесс, масштаб↔качество |
| manufacturing | мощность↔спрос, качество↔себестоимость, гибкость↔стандарт |
| education | содержание↔метод, индивидуальное↔групповое, теория↔практика |
| healthcare | профилактика↔лечение, доступность↔качество, протокол↔индивидуально |
| finance | риск↔доходность, ликвидность↔рост, краткосрочное↔долгосрочное |
| real_estate | локация↔цена, заполняемость↔доходность |
| it_digital | функции↔стабильность, скорость↔качество, пользователь↔технологии |
| consulting | диагностика↔действие, экспертиза↔внедрение |
| personal_project | видение↔ресурсы, действие↔осмысление, самостоятельно↔с партнёрами |

## Символические системы

- **Таро** (Major Arcana) — в `symbolic.py`
- **Ицзин** (выбранные гексаграммы) — `build_iching_catalog()`
- **Социальные/организационные** — `build_social_catalog()`
- **Прямые доменные** — `build_domain_catalog(domain)`

## Использование

```python
from milogic_jev.catalogs_extended import (
    build_domain_catalog,
    build_iching_catalog,
    build_social_catalog,
    list_domains,
)

print(list_domains())

trade = build_domain_catalog("trade")
services = build_domain_catalog("services")
iching = build_iching_catalog()
social = build_social_catalog()
```

Все каталоги совместимы с `SymbolicAdvisor` и обычным `HierarchicalCatalog.evaluate()`.
