UI_CONFIG = {
    "window_title": "Tamer Helper",
    "window_size": "150x350",  # Increased height to accommodate all buttons
    "buttons": [
        ("HEAL", "BANDAGE"),
        ("DISCORD", "FOLLOW"),
        ("MORTAL", "CURE"),
        ("PRI", "SEC"),
        ("EOO", "CW"),
        ("DF", "HONOR"),
    ],
    "settings": {
        "Friend Heal Threshold": 70,
        "Friend Bandage Threshold": 90,
        "Friend Cure Threshold": 50,
        "Pet Heal Threshold": 60,
        "Pet Bandage Threshold": 80,
        "Pet Cure Threshold": 40,
        "Follow Distance": 2,
        "Minimum Mana %": 10,
        "Scan Frequency (ms)": 1000,
        "Healing Method": "Magery",
        "Remove Mortal (Friends)": True,
        "Remove Poison (Friends)": True,
        "Remove Mortal (Pets)": True,
        "Remove Poison (Pets)": True,
        "Use Veterinary": True,
        "Use Bandages (Friends)": True,
        "EOO Threshold": 80,
        "Primary Threshold": 70,
        "Secondary Threshold": 60,
        "CW Threshold": 50,
        "DF Threshold": 10,
        "Honor Threshold": 10,
    },
    "settings_window": {
        "title": "Settings",
        "size": "800x850",
        "sections": {
            "shared": "Shared Settings",
            "friends": "Friends Settings",
            "pets": "Pets Settings"
        },
        "dropdown_settings": [
            {
                "name": "Healing Method",
                "options": ["Magery", "Chivalry"]
            }
        ]
    },
    "numeric_settings": [
        "Friend Heal Threshold", "Friend Bandage Threshold", "Friend Cure Threshold",
        "Pet Heal Threshold", "Pet Bandage Threshold", "Pet Cure Threshold",
        "Follow Distance", "Minimum Mana %", "Scan Frequency (ms)",
        "EOO Threshold", "Primary Threshold", "Secondary Threshold",
        "CW Threshold", "DF Threshold", "Honor Threshold"
    ],
    "boolean_settings": [
        "Remove Mortal (Friends)", "Remove Poison (Friends)",
        "Remove Mortal (Pets)", "Remove Poison (Pets)",
        "Use Veterinary", "Use Bandages (Friends)"
    ],
    "shared_settings": [
        "Follow Distance", "Minimum Mana %", "Scan Frequency (ms)",
        "EOO Threshold", "Primary Threshold", "Secondary Threshold",
        "CW Threshold", "DF Threshold", "Honor Threshold"
    ],
    "friend_settings": ["Friend Heal Threshold", "Friend Bandage Threshold", "Friend Cure Threshold",
                        "Remove Mortal (Friends)", "Remove Poison (Friends)", "Use Bandages (Friends)"],
    "pet_settings": ["Pet Heal Threshold", "Pet Bandage Threshold", "Pet Cure Threshold",
                     "Remove Mortal (Pets)", "Remove Poison (Pets)", "Use Veterinary"],
    "list_sections": ["Friends", "Pets"],
    "state_keys": [
        "HEAL", "BANDAGE", "DISCORD", "FOLLOW",
        "MORTAL", "CURE", "PRI", "SEC",
        "EOO", "CW", "DF", "HONOR"
    ],
    "list_keys": ["FRIENDS", "PETS"],
    "follow_key": "FOLLOW",
    "damage_counter": {
        "position": "right",  # Position the damage counter on the right side
        "width": 20,  # Width of the damage counter display
        "height": 5,  # Height of the damage counter display
    }
}