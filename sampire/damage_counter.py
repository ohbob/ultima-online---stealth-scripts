import datetime

from py_stealth import *
from collections import deque

damage_counter = {
    'enemy': 0,
    'name': '',
    'started': None,
    'ended': None,
    'damage_received': [],
    'damage_done': [],
    'recent_damages': deque(maxlen=10),
    'is_active': False,
    'last_check_time': datetime.datetime.now()
}

def format_time(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    if minutes > 0:
        return f"{minutes}min {seconds}sec"
    else:
        return f"{seconds}sec"

def damage(id, amount):
    current_target = WarTargetID()
    if current_target != 0:
        if damage_counter['enemy'] != current_target:
            reset_damage_counter()
            damage_counter['enemy'] = current_target
            damage_counter['started'] = datetime.datetime.now()
            damage_counter['name'] = GetName(current_target)
            damage_counter['is_active'] = True
        if id == Self():
            damage_counter['damage_received'].append(amount)
            damage_counter['recent_damages'].appendleft(f"[{amount}] [  ]")
        else:
            damage_counter['damage_done'].append(amount)
            damage_counter['recent_damages'].appendleft(f"[  ] [{amount}]")
        print(f"Debug: New damage entry: {damage_counter['recent_damages'][0]}")  # Debug output
    damage_counter['last_check_time'] = datetime.datetime.now()

def reset_damage_counter():
    damage_counter['enemy'] = 0
    damage_counter['name'] = ''
    damage_counter['started'] = None
    damage_counter['ended'] = None
    damage_counter['damage_received'] = []
    damage_counter['damage_done'] = []
    damage_counter['recent_damages'].clear()
    damage_counter['is_active'] = False

def get_damage_counter_info():
    current_target = WarTargetID()
    current_time = datetime.datetime.now()

    # Check if the target has changed or disappeared
    if current_target == 0 and damage_counter['is_active']:
        damage_counter['ended'] = current_time
        damage_counter['is_active'] = False

    total_dmg_received = sum(damage_counter['damage_received'])
    total_dmg_done = sum(damage_counter['damage_done'])
    
    if damage_counter['started']:
        if damage_counter['is_active']:
            total_time = (current_time - damage_counter['started']).total_seconds()
        else:
            total_time = (damage_counter['ended'] - damage_counter['started']).total_seconds()
        dps = total_dmg_done / total_time if total_time > 0 else 0
        drps = total_dmg_received / total_time if total_time > 0 else 0
    else:
        total_time = 0
        dps = 0
        drps = 0

    formatted_time = format_time(total_time)
    status = "Killed: " if not damage_counter['is_active'] and damage_counter['enemy'] != 0 else "Target: "

    return {
        'status': status,
        'name': damage_counter['name'],
        'total_dmg_done': total_dmg_done,
        'total_dmg_received': total_dmg_received,
        'dps': dps,
        'drps': drps,
        'time': formatted_time,
        'recent_damages': list(damage_counter['recent_damages']),
        'is_active': damage_counter['is_active']
    }

def update_damage_counter():
    return get_damage_counter_info()

SetEventProc('evwardamage', damage)