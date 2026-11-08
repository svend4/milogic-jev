# Носители (alice-snov) как домен в milogic-jev

## Закон

Один носитель — два режима.  
Внутри объекта: **50 + 50 = 100**.  
Между двумя полными чтениями возможно 200%.

## Каталог

`carriers.py` содержит 12 носителей из GDD alice-snov:

| id | Объект | Геометрия | Режим A | Режим B | Zero |
|----|--------|-----------|---------|---------|------|
| ski_rocker | Кресло-лыжи | кривая | осцилляция | трансляция | снятые ботинки |
| phase_wheel | Вело-часы | круг+цепь | катить | тикать | снятая цепь |
| opcode_dial | Часы-приборы | вал | резать | черпать | пустой циферблат |
| chandelier | Люстра-фонтан | рожок | светить | стекать | потухший фитиль |
| ship_needle | Корабль в игле | сечение | остаться | пройти | закрытая пробоина |
| book_stairs | Лестница-книги | ступень | идти | миновать ряд | закрытая книга |
| tray_face | Поднос-лицо | плоскость | собрать | быть лицом | пустой поднос |
| hat | Шляпа | цилиндр | надеть | разложить | пустой цилиндр |
| snowflake | Снежинка | дендрит | вверх | падение | молчание |
| white_friend | Белый друг | порог | неверная дверь | карта | закрытый порог |
| assol | Ассоль | берег | ждать | остановить | пустой берег |
| honest_bus | Уходит Бог | шина | один канал | отбросить | молчание шины |

## Использование

```python
from milogic_jev.carriers import build_carrier_catalog
from milogic_jev.symbolic import SymbolicAdvisor
from milogic_jev.carrier_scenes import CarrierSceneLayer

cat = build_carrier_catalog(max_carriers=6)
advisor = SymbolicAdvisor(cat)
results = advisor.catalog.evaluate(state, evaluator)

layer = CarrierSceneLayer()
scenes = layer.enrich(results)

for s in scenes:
    print(s["scene"])
```

## Слои

- `carriers.py` — каталог носителей как монад
- `carrier_scenes.py` — сцены с явным zero и аппаратом
- Совместимо с `MicroArchetypeLayer`, `RefinementOrchestrator` и пайплайном

Источник: [svend4/alice-snov](https://github.com/svend4/alice-snov)
