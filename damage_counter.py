import datetime

from py_stealth import *

damage_counter = {
    'enemy': 0,
    'name': '',
    'started': None,
    'ended': None,
    'damage_recieved': [],
    'damage_done': []
}


def damage(id, amount):
    if WarTargetID() != 0:
        if damage_counter['enemy'] == 0:
            damage_counter['enemy'] = WarTargetID()
            damage_counter['started'] = datetime.datetime.now()
            damage_counter['name'] = GetName(WarTargetID())
        if id == Self():
            damage_counter['damage_recieved'].append(amount)
            print(f"[{amount}] [  ]")
        else:
            damage_counter['damage_done'].append(amount)
            print(f"[  ] [{amount}]")


def reset_and_print_stats():
    name = damage_counter['name']
    damage_counter['ended'] = datetime.datetime.now()
    total_time = (damage_counter['ended'] - damage_counter['started']).total_seconds()
    total_dmg_received = sum(damage_counter['damage_recieved'])
    total_dmg_done = sum(damage_counter['damage_done'])
    dps = total_dmg_done / total_time
    drps = total_dmg_received / total_time
    print(f"DPS: {dps:.2f}, DRPS: {drps:.2f}")
    print(f"Time to kill {name}: {total_time:.2f} seconds")
    print("\n----------------")
    damage_counter['enemy'] = 0
    damage_counter['started'] = None
    damage_counter['ended'] = None
    damage_counter['name'] = ""
    damage_counter['damage_recieved'] = []
    damage_counter['damage_done'] = []


SetEventProc('evwardamage', damage)

while True:
    if WarTargetID() == 0 and damage_counter['enemy'] != 0 and not IsObjectExists(damage_counter['enemy']):
        reset_and_print_stats()
    Wait(100)