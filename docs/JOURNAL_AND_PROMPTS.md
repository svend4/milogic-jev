# Журнал замыканий и промпты сцен

## Журнал (`journal.py`)

Записывает сильные монады в JSONL.

```python
from milogic_jev.journal import JournalRecorder, summary

rec = JournalRecorder("journal.jsonl")
n = rec.record_results("services", level_results)
print(summary("journal.jsonl"))
```

## Промпты (`prompts.py`)

Генерирует короткие текстовые промпты для изображения.

```python
from milogic_jev.prompts import prompts_from_micro, prompts_from_carriers

# из микро-архетипов
prompts = prompts_from_micro(enriched_items)

# из носителей
prompts = prompts_from_carriers(carrier_scenes)
```

Оба слоя не меняют расчёт.  
Журнал накапливает историю. Промпты готовят визуальный слой.
