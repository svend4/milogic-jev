# CLI и сравнение доменов

## CLI

```bash
python -m milogic_jev.cli domains
python -m milogic_jev.cli carriers
python -m milogic_jev.cli run --domain services --state "Спрос растёт"
python -m milogic_jev.cli compare services trade
```

## Сравнение

```python
from milogic_jev.compare import compare_domains, all_domain_summary

print(all_domain_summary())
print(compare_domains("services", "finance"))
```

CLI использует мок-оценщик. Для реального Jev замените `mock_evaluator` в `cli.py`.
