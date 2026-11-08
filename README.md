# Milogic-Jev

Новые классы систем принятия решений, сочетающие:

- структурированные типизированные вопросы и калибровку (принцип Jev / System One),
- иерархию двойственных отношений, замыкание и «образ и подобие» (принципы милогии М.И. Беляева).

## Структура

```
milogic_jev/
  core.py              # основные классы
  STEP_BY_STEP.md      # поэтапная реализация
  README.md
docs/
  milogic_jev_classes.md         # таксономия всех классов и подвидов
  milogic_jev_implementable.md   # схемы, JSON/YAML, примеры
```

## Быстрый старт

```python
from milogic_jev.core import build_belyaev_core_catalog

catalog = build_belyaev_core_catalog()

def your_jev_evaluator(state: str, questions: dict) -> dict:
    # вызов реального API Jev или аналога
    ...

result = catalog.evaluate(
    state="Ваш фрагмент текста или описание двойственности",
    evaluator=your_jev_evaluator
)
```

## Основные классы

1. Иерархический каталог вопросов (оболочки)
2. Монадные вопросы (новый примитив)
3. Генеративные каталоги
4. Смена системы отсчёта
5. Композиция через замыкание
6. Многоуровневое состояние
7. Калибровка двойственностей
8. Гибриды

Подробности — в `docs/` и `milogic_jev/STEP_BY_STEP.md`.
