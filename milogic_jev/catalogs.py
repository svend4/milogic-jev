"""
Concrete catalogs of dualities drawn from Belyaev's Milogiya texts.
These can be loaded into HierarchicalCatalog or used as question templates.
"""

from typing import Dict, List, Any

# Level 0–1: Chemical elements and periodic system
CHEMICAL_HIERARCHY = {
    "id": "chemical_hierarchy",
    "description": "Атом водорода → периодическая система → ядерные оболочки",
    "levels": [
        {
            "id": "L0_hydrogen",
            "questions": {
                "hydrogen_as_basis": {
                    "type": "monad",
                    "pole_a": "атом водорода (замысел)",
                    "pole_b": "периодическая система (смысл)",
                    "criteria": "Является ли атом водорода достаточным базисом для порождения периодической системы по милогии"
                }
            }
        },
        {
            "id": "L1_periodic",
            "depends_on": ["L0_hydrogen"],
            "questions": {
                "periodic_as_shell": {
                    "type": "score",
                    "min": 0,
                    "max": 10,
                    "criteria": "Насколько периодическая система является замкнутой оболочкой 2-го уровня иерархии"
                },
                "nuclear_follows": {
                    "type": "noul",
                    "criteria": "Ядерные оболочки естественно следуют как следующий уровень"
                }
            }
        }
    ]
}

PARTICLE_HIERARCHY = {
    "id": "particle_hierarchy",
    "description": "Элементарные частицы как 1-й уровень иерархии материи",
    "levels": [
        {
            "id": "L0_particles",
            "questions": {
                "particles_level": {
                    "type": "choice",
                    "options": [
                        "1-й уровень иерархии",
                        "0-й уровень (кварки/эфир)",
                        "переходный",
                        "не определён"
                    ],
                    "criteria": "К какому уровню иерархии материи относятся элементарные частицы относительно химических элементов"
                },
                "duality_proton_neutron": {
                    "type": "monad",
                    "pole_a": "протоны",
                    "pole_b": "нейтроны",
                    "criteria": "Двойственность протонных и нейтронных оболочек"
                }
            }
        }
    ]
}

SOCIAL_HIERARCHY = {
    "id": "social_hierarchy",
    "description": "Распространение законов иерархии на социальные организмы и Коллективный Разум",
    "levels": [
        {
            "id": "L0_social_duality",
            "questions": {
                "individual_collective": {
                    "type": "monad",
                    "pole_a": "индивидуальный разум",
                    "pole_b": "коллективный разум",
                    "criteria": "Двойственность индивидуального и коллективного разума по законам иерархии"
                }
            }
        },
        {
            "id": "L1_integration",
            "depends_on": ["L0_social_duality"],
            "questions": {
                "integration_viable": {
                    "type": "noul",
                    "criteria": "Возможна ли устойчивая интеграция в Коллективный Разум без нарушения ограниченности уровней"
                }
            }
        }
    ]
}

SYMMETRY_DUALITIES = [
    {
        "id": "symmetry_asymmetry",
        "pole_a": "симметрия",
        "pole_b": "асимметрия",
        "criteria": "Единство и переход симметрии и асимметрии на разных уровнях иерархии"
    },
    {
        "id": "form_content",
        "pole_a": "форма",
        "pole_b": "содержание",
        "criteria": "Двойственность формы и содержания"
    },
    {
        "id": "intention_meaning",
        "pole_a": "замысел",
        "pole_b": "смысл",
        "criteria": "Трансформация замысла в смысл"
    },
    {
        "id": "integration_differentiation",
        "pole_a": "интеграция",
        "pole_b": "дифференциация",
        "criteria": "Эволюционная интеграция и инволюционная дифференциация"
    }
]


def get_all_catalogs() -> Dict[str, Dict]:
    return {
        "chemical": CHEMICAL_HIERARCHY,
        "particle": PARTICLE_HIERARCHY,
        "social": SOCIAL_HIERARCHY,
    }


def get_symmetry_dualities() -> List[Dict[str, str]]:
    return SYMMETRY_DUALITIES


def as_jev_questions(duality: Dict[str, str]) -> Dict[str, Any]:
    return {
        duality["id"]: {
            "type": "monad",
            "pole_a": duality["pole_a"],
            "pole_b": duality["pole_b"],
            "criteria": duality["criteria"]
        }
    }
