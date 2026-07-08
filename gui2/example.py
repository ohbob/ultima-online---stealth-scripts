from py_stealth import *
from ui_list import Assistant, launch


def cast_spell(spell, mana, on='self', *, target=None, no_buff=None, if_buff=None, war=False, in_fight=False):
    if not Connected() or Dead(): return
    if war and not IsWarMode(Self()): return
    if Mana() < mana: return

    buffs = [GetClilocByID(b['ClilocID1']).upper() for b in GetBuffBarInfo()]
    if if_buff and not any(if_buff.upper() in b for b in buffs): return
    if no_buff and any(no_buff.upper() in b for b in buffs): return

    if in_fight:
        t = WarTargetID()
        if t <= 0 or t == Self() or IsDead(t): return

    if target is not None:
        mobile_id = target
    elif on == 'self':
        mobile_id = Self()
    elif on == 'war':
        mobile_id = WarTargetID()
    elif on == 'last':
        mobile_id = LastTarget()
    else:
        mobile_id = on

    if mobile_id <= 0 or (mobile_id != Self() and IsDead(mobile_id)): return
    CastToObj(spell, mobile_id)
    Wait(50)

class Bushido:
    def lightning_strike():
        cast_spell('Lightning Strike', 10, on='self', no_buff='Lightning Strike', war=True)

    def counter_attack():
        cast_spell('Counter Attack', 5, on='self', no_buff='Counter', war=True)



class Chivalry:
    def enemy_of_one():
        cast_spell('Enemy of One', 16, on='self', no_buff='Enemy of One', war=True)

    def consecrate_weapon():
        cast_spell('Consecrate Weapon', 11, on='self', no_buff='Consecrate', if_buff='Enemy of One', in_fight=True)

Assistant('Chivalry', [
    ['Enemy of One', Chivalry.enemy_of_one, 200],
    ['Consecrate Weapon', Chivalry.consecrate_weapon, 200],
])

Assistant('Bushido', [
    ['Lightning Strike', Bushido.lightning_strike, 200],
    ['Counter Attack', Bushido.counter_attack, 200],
])


launch()
