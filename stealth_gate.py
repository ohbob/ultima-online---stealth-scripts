from py_stealth import *

TARGET_HIDING = 100
TARGET_STEALTH = 100
TARGET_NINJITSU = 100

gatetype = 0x0F6C

armor_sets = {
    'ringmail': {
        'arms': {'type': 0x13EE, 'skill': 50, 'layer': ArmsLayer()},
        'legs': {'type': 0x13F0, 'skill': 60, 'layer': PantsLayer()},
        'tunic': {'type': 0x13EC, 'skill': 69, 'layer': ShirtLayer()},
    },
    'chainmail': {
        'helmet': {'type': 0x13BB, 'skill': 70, 'layer': HatLayer()},
        'legs': {'type': 0x13BE, 'skill': 72, 'layer': PantsLayer()},
    },
    'plate': {
        # 'gorget': {'type': 0x1413, 'skill': 90, 'layer': NeckLayer()}, # didnt buy it
        'legs': {'type': 0x13BE, 'skill': 72, 'layer': PantsLayer()}, # chainmail leggs
        'helmet': {'type': 0x1412, 'skill': 92, 'layer': HatLayer()},
        'gloves': {'type': 0x1414, 'skill': 94, 'layer': GlovesLayer()},
        'arms': {'type': 0x1410, 'skill': 94, 'layer': GlovesLayer()},
        'tunic': {'type': 0x13EC, 'skill': 98, 'layer': ShirtLayer()}, # add the ringmail tunic
        # 'legs': {'type': 0x1411, 'skill': 96, 'layer': PantsLayer()}, # 90 str too much 
    }
}

def get_current_armor_set():
    stealth_skill = GetSkillValue('Stealth')
    if stealth_skill >= 90:
        return armor_sets['plate']
    elif stealth_skill >= 70:
        return armor_sets['chainmail']
    else:
        return armor_sets['ringmail']

def gate(radio, btn):
    SetFindVertical(20)
    SetFindDistance(3)
    if FindType(0x0F6C, Ground()) > 0:
        UseObject(FindItem())
        CheckLag(500)
        NumGumpRadiobutton(GetGumpsCount() - 1, radio, btn)
        NumGumpButton(GetGumpsCount()-1, 1)
        CheckLag(500)

def REquip():
    current_armor_set = get_current_armor_set()
    for item_info in current_armor_set.values():
        if GetSkillValue('Stealth') >= item_info['skill']:
            if not ObjAtLayer(item_info['layer']) or GetType(ObjAtLayer(item_info['layer'])) != item_info['type']:
                FindTypeEx(item_info['type'], 0xFFFF, Backpack(), False)
                if FindQuantity() > 0:
                    UnEquip(item_info['layer'])
                    Wait(650)
                    Equip(item_info['layer'], FindItem())
                    Wait(650)

def GateTrain():
    radios = [1, 2]
    while True:
        if (GetSkillValue('Stealth') >= TARGET_STEALTH and
            GetSkillValue('Ninjitsu') >= 87.5):
            return
        
        REquip()
        for r in radios:
            gate(r, 1)
            gateobj = FindType(gatetype, Ground())
            if gateobj > 0:
                gate_x, gate_y = GetX(gateobj), GetY(gateobj)
                NewMoveXY(gate_x, gate_y + 1, False, 0, False)
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if not Hidden():
                            break
                        if (Mana() > 15 and GetSkillValue('Stealth') > 60 and 
                            GetSkillValue('Ninjitsu') > 44 and GetSkillValue('Ninjitsu') < 87.5):
                            Cast("Shadow Jump")
                            WaitForTarget(1000)
                            if TargetPresent():
                                TargetToXYZ(gate_x + dx, gate_y + dy, GetZ(Self()))
                                Wait(500) # recovery
                        else:
                            NewMoveXY(gate_x + dx, gate_y + dy, False, 0, False)
                        if GetSkillValue('Ninjitsu') > 40 and GetSkillValue('Ninjitsu') < 57.5 and Mana() > 15 and PetsCurrent() < MaxPets():
                            Cast("Mirror image")
                        if not Hidden() and GetSkillValue('Hiding') < TARGET_HIDING:
                            UseSkill("Hiding")
                if not Hidden() and GetSkillValue('Hiding') < TARGET_HIDING:
                    UseSkill("Hiding")
        
        # Undress armor if stealth skill has reached the target
        if GetSkillValue('Stealth') >= TARGET_STEALTH:
            for armor_set in armor_sets.values():
                for item_info in armor_set.values():
                    if ObjAtLayer(item_info['layer']):
                        UnEquip(item_info['layer'])
                        Wait(650)

GateTrain()