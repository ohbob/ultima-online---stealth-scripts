"""Animal Taming rail script — works at any spawn location.

Edit RAIL with waypoints for your hunting spot (coordinates + labels).
ANIMALS is regenerated from ServUO via scripts/generate_mobiles.py.
bodies_for_skill() picks gain-window targets from the full tameable list.

Gain window: GAIN_WINDOW skill points below current skill (not percent).
At 30.0 taming, targets min_tame 20.0–30.0 — e.g. hind (23.1) on Trinsic beach.
"""
from datetime import datetime, timedelta
from py_stealth import *

SKILL = 'Animal Taming'
GOAL = 120.0
GAIN_WINDOW = 10.0  # skill points below current — at 30 tames min_tame 20.0 to 30.0
TAME_TIMEOUT = 25          # idle seconds since last start/Good before giving up
TAME_START_WAIT = 5
TAME_RETRIES = 30
TARGET_WAIT_MS = 2000
KILL_TIMEOUT = 25
FIND_DISTANCE = 40
FIND_VERTICAL = 40

# Stealth journal lines (ServUO AnimalTaming.cs clilocs) — example from live client:
#   [03:10:59:523] System: System Tame which animal?              (502789)
#   [03:10:59:583] Flow: Flow *You start to tame the creature.*  (1010597 emote)
#   [03:11:02:746] Flow: Flow Good...                             (502790-502793 progress)
#   [03:11:06:026] Flow: Flow Good...
#   [03:11:09:052] a hind: a hind You fail to tame the creature.  (502798)
# Success: It seems to accept you as master. (502799)
JOURNAL_TARGET = 'Tame which animal'
JOURNAL_STARTED = 'start to tame the creature|You start to tame'
JOURNAL_GOOD = 'Good'
JOURNAL_TAMED = 'accept you as|seems to accept you'
JOURNAL_FAIL = 'fail to tame the creature'
JOURNAL_RETRY = (
    'fail to tame the creature|clear path|too far away to continue|'
    'anger the beast|too angry to continue|been distracted'
)
JOURNAL_ABORT = (
    'Someone else is already taming|cannot be tamed|looks tame already|'
    'You can\'t tame that|no chance of taming|That is too far away'
)
JOURNAL_TOO_MANY = 'too many followers'

# Hunting rail — move to each stop, tame nearby animals, repeat until GOAL
# Example below is Trinsic beach; replace with your area's waypoints
RAIL = [
    (2118, 2795, 'stop 1'),
    (2115, 2778, 'stop 2'),
    (2113, 2745, 'stop 3'),
    (2113, 2709, 'stop 4'),
    (2103, 2685, 'stop 5'),
    (2083, 2661, 'stop 6'),
]

# ServUO: Scripts/Mobiles — body ID + MinTameSkill (regenerate with generate_mobiles.py)
# BEGIN ANIMALS (generated — do not edit)
ANIMALS = [
    {'name': 'dog', 'body': 0x00D9, 'min_tame': -21.3},
    {'name': 'ferret', 'body': 0x0117, 'min_tame': -21.3},
    {'name': 'squirrel', 'body': 0x0116, 'min_tame': -21.3},
    {'name': 'gorilla', 'body': 0x001D, 'min_tame': -18.9},
    {'name': 'jack_rabbit', 'body': 0x00CD, 'min_tame': -18.9},
    {'name': 'mongbat', 'body': 0x0027, 'min_tame': -18.9},
    {'name': 'rabbit', 'body': 0x00CD, 'min_tame': -18.9},
    {'name': 'skittering_hopper', 'body': 0x012E, 'min_tame': -12.9},
    {'name': 'bird', 'body': 0x0006, 'min_tame': -6.9},
    {'name': 'cat', 'body': 0x00C9, 'min_tame': -0.9},
    {'name': 'chicken', 'body': 0x00D0, 'min_tame': -0.9},
    {'name': 'mountain_goat', 'body': 0x0058, 'min_tame': -0.9},
    {'name': 'rat', 'body': 0x00EE, 'min_tame': -0.9},
    {'name': 'sewerrat', 'body': 0x00EE, 'min_tame': -0.9},
    {'name': 'battle_chicken_lizard', 'body': 0x02CC, 'min_tame': 0.0},
    {'name': 'chicken_lizard', 'body': 0x02CC, 'min_tame': 0.0},
    {'name': 'parrot', 'body': 0x033F, 'min_tame': 0.0},
    {'name': 'cow', 'body': 0x00D8, 'min_tame': 11.1},
    {'name': 'cow', 'body': 0x00E7, 'min_tame': 11.1},
    {'name': 'goat', 'body': 0x00D1, 'min_tame': 11.1},
    {'name': 'pig', 'body': 0x00CB, 'min_tame': 11.1},
    {'name': 'sheep', 'body': 0x00CF, 'min_tame': 11.1},
    {'name': 'eagle', 'body': 0x0005, 'min_tame': 17.1},
    {'name': 'lowland_boura', 'body': 0x02CB, 'min_tame': 19.1},
    {'name': 'ruddy_boura', 'body': 0x02CB, 'min_tame': 19.1},
    {'name': 'bull_frog', 'body': 0x0051, 'min_tame': 23.1},
    {'name': 'corrosive_slime', 'body': 0x0033, 'min_tame': 23.1},
    {'name': 'hind', 'body': 0x00ED, 'min_tame': 23.1},
    {'name': 'slime', 'body': 0x0033, 'min_tame': 23.1},
    {'name': 'timber_wolf', 'body': 0x00E1, 'min_tame': 23.1},
    {'name': 'boar', 'body': 0x0122, 'min_tame': 29.1},
    {'name': 'giant_rat', 'body': 0x00D7, 'min_tame': 29.1},
    {'name': 'pack_horse', 'body': 0x0123, 'min_tame': 29.1},
    {'name': 'pack_llama', 'body': 0x0124, 'min_tame': 29.1},
    {'name': 'black_bear', 'body': 0x00D3, 'min_tame': 35.1},
    {'name': 'llama', 'body': 0x00DC, 'min_tame': 35.1},
    {'name': 'polar_bear', 'body': 0x00D5, 'min_tame': 35.1},
    {'name': 'walrus', 'body': 0x00DD, 'min_tame': 35.1},
    {'name': 'brown_bear', 'body': 0x00A7, 'min_tame': 41.1},
    {'name': 'cougar', 'body': 0x003F, 'min_tame': 41.1},
    {'name': 'deathwatch_beetle', 'body': 0x00F2, 'min_tame': 41.1},
    {'name': 'alligator', 'body': 0x00CA, 'min_tame': 47.1},
    {'name': 'high_plains_boura', 'body': 0x02CB, 'min_tame': 47.1},
    {'name': 'scorpion', 'body': 0x0030, 'min_tame': 47.1},
    {'name': 'grey_wolf', 'body': 0x0019, 'min_tame': 53.1},
    {'name': 'grey_wolf', 'body': 0x001B, 'min_tame': 53.1},
    {'name': 'panther', 'body': 0x00D6, 'min_tame': 53.1},
    {'name': 'snow_leopard', 'body': 0x0040, 'min_tame': 53.1},
    {'name': 'snow_leopard', 'body': 0x0041, 'min_tame': 53.1},
    {'name': 'giant_spider', 'body': 0x001C, 'min_tame': 59.1},
    {'name': 'great_hart', 'body': 0x00EA, 'min_tame': 59.1},
    {'name': 'grizzly_bear', 'body': 0x00D4, 'min_tame': 59.1},
    {'name': 'snake', 'body': 0x0034, 'min_tame': 59.1},
    {'name': 'wolf_spider', 'body': 0x02E0, 'min_tame': 59.1},
    {'name': 'gargoyle_pet', 'body': 0x02DA, 'min_tame': 65.1},
    {'name': 'stone_slith', 'body': 0x02DE, 'min_tame': 65.1},
    {'name': 'white_wolf', 'body': 0x0022, 'min_tame': 65.1},
    {'name': 'white_wolf', 'body': 0x0025, 'min_tame': 65.1},
    {'name': 'gaman', 'body': 0x00F8, 'min_tame': 68.7},
    {'name': 'bull', 'body': 0x00E8, 'min_tame': 71.1},
    {'name': 'bull', 'body': 0x00E9, 'min_tame': 71.1},
    {'name': 'giant_ice_worm', 'body': 0x0059, 'min_tame': 71.1},
    {'name': 'greater_mongbat', 'body': 0x0027, 'min_tame': 71.1},
    {'name': 'hell_cat', 'body': 0x00C9, 'min_tame': 71.1},
    {'name': 'iron_beetle', 'body': 0x02CA, 'min_tame': 71.1},
    {'name': 'strong_mongbat', 'body': 0x0027, 'min_tame': 71.1},
    {'name': 'blood_fox', 'body': 0x058F, 'min_tame': 72.0},
    {'name': 'ossein_ram', 'body': 0x0591, 'min_tame': 72.0},
    {'name': 'frost_spider', 'body': 0x0014, 'min_tame': 74.7},
    {'name': 'giant_toad', 'body': 0x0050, 'min_tame': 77.1},
    {'name': 'bake_kitsune', 'body': 0x00F6, 'min_tame': 80.7},
    {'name': 'lava_lizard', 'body': 0x00CE, 'min_tame': 80.7},
    {'name': 'slith', 'body': 0x02DE, 'min_tame': 80.7},
    {'name': 'dire_wolf', 'body': 0x0017, 'min_tame': 83.1},
    {'name': 'imp', 'body': 0x004A, 'min_tame': 83.1},
    {'name': 'drake', 'body': 0x003C, 'min_tame': 84.3},
    {'name': 'drake', 'body': 0x003D, 'min_tame': 84.3},
    {'name': 'crimson_drake', 'body': 0x058B, 'min_tame': 85.0},
    {'name': 'crimson_drake', 'body': 0x058C, 'min_tame': 85.0},
    {'name': 'platinum_drake', 'body': 0x0589, 'min_tame': 85.0},
    {'name': 'platinum_drake', 'body': 0x058A, 'min_tame': 85.0},
    {'name': 'stygian_drake', 'body': 0x058E, 'min_tame': 85.0},
    {'name': 'hell_hound', 'body': 0x0062, 'min_tame': 85.5},
    {'name': 'ice_hound', 'body': 0x0062, 'min_tame': 85.5},
    {'name': 'predator_hell_cat', 'body': 0x007F, 'min_tame': 90.0},
    {'name': 'dragon', 'body': 0x000C, 'min_tame': 93.9},
    {'name': 'dragon', 'body': 0x003B, 'min_tame': 93.9},
    {'name': 'rune_beetle', 'body': 0x00F4, 'min_tame': 93.9},
    {'name': 'skree', 'body': 0x02DD, 'min_tame': 95.1},
    {'name': 'cold_drake', 'body': 0x003C, 'min_tame': 96.0},
    {'name': 'cold_drake', 'body': 0x003D, 'min_tame': 96.0},
    {'name': 'dread_spider', 'body': 0x000B, 'min_tame': 96.0},
    {'name': 'lion', 'body': 0x0592, 'min_tame': 96.0},
    {'name': 'tsuki_wolf', 'body': 0x00FA, 'min_tame': 96.0},
    {'name': 'dragon_wolf', 'body': 0x02CF, 'min_tame': 102.0},
    {'name': 'frost_mite', 'body': 0x0590, 'min_tame': 102.0},
    {'name': 'phoenix', 'body': 0x0340, 'min_tame': 102.0},
    {'name': 'sabertoothed_tiger', 'body': 0x0588, 'min_tame': 102.0},
    {'name': 'triceratops', 'body': 0x0587, 'min_tame': 102.0},
    {'name': 'greater_dragon', 'body': 0x000C, 'min_tame': 104.7},
    {'name': 'greater_dragon', 'body': 0x003B, 'min_tame': 104.7},
    {'name': 'frost_dragon', 'body': 0x000C, 'min_tame': 105.0},
    {'name': 'frost_dragon', 'body': 0x003B, 'min_tame': 105.0},
    {'name': 'shadow_wyrm', 'body': 0x006A, 'min_tame': 105.0},
    {'name': 'serpentine_dragon', 'body': 0x0067, 'min_tame': 108.0},
]
# END ANIMALS


def bodies_for_skill(skill_value):
    tameable = [a for a in ANIMALS if a['min_tame'] <= skill_value]
    if not tameable:
        lowest = min(a['min_tame'] for a in ANIMALS)
        bodies = [a['body'] for a in ANIMALS if a['min_tame'] == lowest]
        return list(dict.fromkeys(bodies))

    window_low = skill_value - GAIN_WINDOW
    in_window = [a for a in tameable if window_low <= a['min_tame'] <= skill_value]
    if not in_window:
        best = max(a['min_tame'] for a in tameable)
        in_window = [a for a in tameable if a['min_tame'] == best]

    return list(dict.fromkeys(a['body'] for a in in_window))


def kill_for_release(serial):
    """Kill tamed pet to free a follower slot. Taming leaves peace mode — war on to hit.
    Training client may equip butcher knife/dagger; not required by this script."""
    SetWarMode(True)
    deadline = datetime.now() + timedelta(seconds=KILL_TIMEOUT)
    while Connected() and not Dead() and IsObjectExists(serial) and GetHP(serial) > 0 and datetime.now() < deadline:
        if TargetPresent():
            CancelTarget()
        if GetDistance(serial) > 1:
            NewMoveXY(GetX(serial), GetY(serial), True, 1, True)
        Attack(serial)
        Wait(50)
    SetWarMode(False)


def cast_tame(mob):
    if not IsObjectExists(mob) or GetHP(mob) <= 0:
        return False
    if TargetPresent():
        CancelTarget()
    if IsWarMode(Self()):
        SetWarMode(False)
    UseSkill(SKILL)
    if not WaitForTarget(TARGET_WAIT_MS):
        if TargetPresent():
            CancelTarget()
        return False
    WaitTargetObject(mob)
    if TargetPresent():
        CancelTarget()
        return False
    return True


def kill_if_full():
    if PetsCurrent() < (MaxPets() or 5):
        return True
    for mobile in GetMobiles():
        serial = mobile if isinstance(mobile, int) else getattr(mobile, 'serial', 0) or getattr(mobile, 'Serial', 0)
        if not serial or serial == Self() or not IsObjectExists(serial) or GetHP(serial) <= 0:
            continue
        if 'tame' not in GetTooltip(serial).lower():
            continue
        kill_for_release(serial)
        return True
    return False


def wait_tame_started(cast_t0):
    start_deadline = cast_t0 + timedelta(seconds=TAME_START_WAIT)
    while Connected() and not Dead() and datetime.now() < start_deadline:
        now = datetime.now()
        if InJournalBetweenTimes(JOURNAL_STARTED, cast_t0, now) > 0:
            return now
        Wait(50)
    return None


def wait_tame_outcome(mob, journal_t0):
    last_progress = journal_t0
    while Connected() and not Dead():
        now = datetime.now()
        if not IsObjectExists(mob) or GetHP(mob) <= 0:
            return 'gone'
        if InJournalBetweenTimes(JOURNAL_TAMED, journal_t0, now) > 0:
            Wait(100)
            kill_for_release(mob)
            return 'tamed'
        if InJournalBetweenTimes(JOURNAL_ABORT, journal_t0, now) > 0:
            return 'abort'
        if InJournalBetweenTimes(JOURNAL_TOO_MANY, journal_t0, now) > 0:
            return 'too_many'
        if InJournalBetweenTimes(JOURNAL_FAIL, journal_t0, now) > 0:
            return 'fail'
        if InJournalBetweenTimes(JOURNAL_RETRY, journal_t0, now) > 0:
            return 'retry'
        if InJournalBetweenTimes(JOURNAL_GOOD, last_progress, now) > 0:
            last_progress = now
        idle_s = (now - last_progress).total_seconds()
        if idle_s >= TAME_TIMEOUT:
            return 'timeout'
        if GetDistance(mob) > 1:
            NewMoveXY(GetX(mob), GetY(mob), True, 1, True)
        Wait(50)
    return 'disconnect'


def mob_alive(mob):
    return mob and IsObjectExists(mob) and GetHP(mob) > 0


def move_to_mob(mob):
    while GetDistance(mob) > 1:
        if not Connected() or Dead() or not mob_alive(mob):
            return False
        NewMoveXY(GetX(mob), GetY(mob), True, 1, True)
        Wait(50)
    return mob_alive(mob)


def start_tame(mob):
    """Move, cast, wait for journal start. Returns journal_t0 or None."""
    if not move_to_mob(mob):
        return None
    cast_t0 = datetime.now()
    if not cast_tame(mob):
        return None
    journal_t0 = wait_tame_started(cast_t0)
    if journal_t0 is None:
        if TargetPresent():
            CancelTarget()
        Wait(200)
    return journal_t0


def recast_tame(mob):
    """Recast on same mob after fail/retry/timeout — no start-retry budget."""
    while Connected() and not Dead() and mob_alive(mob):
        journal_t0 = start_tame(mob)
        if journal_t0 is not None:
            return journal_t0
    return None


def find_mob(body_types):
    for body in body_types:
        if FindType(body, Ground()) <= 0:
            continue
        for serial in sorted(GetFindedList(), key=GetDistance):
            if mob_alive(serial):
                return serial
    return 0


def tame_here():
    SetFindDistance(FIND_DISTANCE)
    SetFindVertical(FIND_VERTICAL)
    body_types = bodies_for_skill(GetSkillValue(SKILL))

    while Connected() and not Dead():
        mob = find_mob(body_types)
        if not mob or not kill_if_full():
            return

        journal_t0 = None
        for _ in range(TAME_RETRIES):
            if not mob_alive(mob):
                break
            journal_t0 = start_tame(mob)
            if journal_t0 is not None:
                break

        if not mob_alive(mob):
            if TargetPresent():
                CancelTarget()
            continue

        if journal_t0 is None:
            Ignore(mob)
            if TargetPresent():
                CancelTarget()
            continue

        while Connected() and not Dead() and mob_alive(mob):
            outcome = wait_tame_outcome(mob, journal_t0)

            if outcome == 'tamed':
                while Connected() and not Dead() and mob_alive(mob):
                    kill_for_release(mob)
                break

            if outcome == 'abort':
                Ignore(mob)
                break

            if outcome in ('gone', 'disconnect'):
                break

            if outcome == 'too_many':
                if not kill_if_full():
                    return

            if outcome in ('fail', 'retry', 'timeout', 'too_many'):
                if TargetPresent():
                    CancelTarget()
                Wait(200)
                journal_t0 = recast_tame(mob)
                if journal_t0 is None:
                    break
                continue

            break

        if TargetPresent():
            CancelTarget()


def main():
    while Connected() and not Dead() and GetSkillValue(SKILL) < GOAL:
        for x, y, _label in RAIL:
            if not Connected() or Dead():
                break
            NewMoveXY(x, y, True, 1, True)
            tame_here()


main()
