from typing import Literal

CONSUMABLE_MAP = {
    "BANDAGE": (3617, 0xFFFF),
    "GREATER EXPLOSION": (3853, 0),
    "GREATER STRENGTH": (3849, 0),
    "GREATER HEAL": (3852, 0),
    "GREATER REFRESHMENT": (3851, 0),
    "GREATER AGILITY": (3848, 0),
    "GREATER CURE": (3847, 0),
    "GREATER CONFLAGRATION": (3846, 1161),
    "GREATER CONFUSION BLAST": (3846, 1165),
    "INVISIBILITY": (3846, 306),
    "SMOKE BOMB": (10248, 0),
    "ENCHANTED APPLE": (12248, 1160),
    "BOLAS": (9900, 0),
    "ORANGE PETALS": (4129, 43),
    "ROSE OF TRINSIC": (4129, 14),
    "GRAPES OF WRATH": (12247, 1154),
    "RECALL": (8012, 0),
}

ConsumableType = Literal[
    "GREATER EXPLOSION", "GREATER STRENGTH", "GREATER HEAL", "GREATER REFRESHMENT",
    "GREATER AGILITY", "GREATER CURE", "GREATER CONFLAGRATION", "GREATER CONFUSION BLAST",
    "INVISIBILITY", "SMOKE BOMB", "ENCHANTED APPLE", "BOLAS", "ORANGE PETALS",
    "ROSE OF TRINSIC", "GRAPES OF WRATH", "RECALL", "BANDAGE"
]