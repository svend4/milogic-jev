# Все варианты классов — карта реализации

Реализации находятся в `milogic_jev/variants.py`.

| Класс | Вариант | Класс в коде |
|-------|---------|--------------|
| 1. Hierarchical Shells | Fixed | `FixedShellCatalog` |
| 1 | Dynamic | базовый `HierarchicalCatalog` |
| 1 | Nested | `NestedSubshellCatalog` |
| 2. Monad | Static | `MonadAnswer` + `MonadQuestionBuilder` |
| 2 | Open | `OpenMonadBuilder` |
| 2 | Multi | `MultiMonadEvaluator` |
| 2 | Temporal | `TemporalMonad` |
| 3. Generative | Inheritance / Closure | `GenerativeCatalog` |
| 3 | Evolutionary selection | `EvolutionarySelector` |
| 3 | Bounded growth | `BoundedGrowthCatalog` |
| 4. Reference Frame | Parallel | `ReferenceFrameEvaluator` |
| 4 | Invariant search | `InvariantSearcher` |
| 4 | Adaptive | `AdaptiveFrameEvaluator` |
| 5. Closure composition | — | `ClosureComposer` |
| 6. Multi-level state | — | `MultiLevelState` + `MultiLevelEvaluator` |
| 7. Calibration | — | `DualityCalibrationLog` |
| 8. Hybrid | Orchestrator | `HybridOrchestrator` |

Демонстрация: `python -m milogic_jev.demo_variants`
