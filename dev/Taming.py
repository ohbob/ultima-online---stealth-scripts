''' Script Name: Trinsic Tamer
 Author: Camo
 Version: 0.3 Beta
 Client Tested with: 7.0.20.0
 Stealth version tested with: 8.9.5
 Shard OSI / FS: http://uoinfinity.net/
 Revision Date: 2019/05/29
 Public Release: 2019/05/29
 Notes: Get 30 taming, bunch of butchers knifes, daggers and clubs and head to trinsic north east shore and press play.

 Revision. 0.3 -- Added the right animal skill requirements for all the animals in the area, added training weapons.
 Revision. 0.2 -- Added timeouts, to not get stuck, just in case.
 Revision. 0.3 -- Added too far message and a cow that was missing with a second bull type.
'''

from datetime import datetime, timedelta
from py_stealth import *

# Constants
RELEASE_GUMP = 2426193729
RELEASE_BUTTON = 2
MAX_PETS = 5
TAMING_TIMEOUT = 20
RELEASE_TIMEOUT = 20
TARGET_SKILL = 105.0


def wait_for_gump(gump_id, button_number=0, press_button=True, timeout=15):
    end_time = datetime.now() + timedelta(seconds=timeout)
    while datetime.now() < end_time:
        if IsGump():
            for gump_index in range(GetGumpsCount()):
                gump_info = GetGumpInfo(gump_index)
                if 'GumpID' in gump_info and gump_info['GumpID'] == gump_id:
                    if press_button:
                        NumGumpButton(gump_index, button_number)
                    else:
                        return gump_info
                    return True
                if IsGumpCanBeClosed(gump_index):
                    CloseSimpleGump(gump_index)
        CheckLag(5000)
    return False

def get_animals_by_skill(skill):
    # if skill < 30:
    #     return (0x00E4, 0x00C8, 0x00CC, 0x00E2, 0x00CD, 0x0006)  # rabbit, birds
    # elif skill < 50:
    #     return (0x00E4, 0x00C8, 0x00CC, 0x00E2, 0x00CD, 0x0006, 0x00CF, 0x00D8, 0x00E7)  # + sheep, cow
    # elif skill < 70:
    #     return  (0x00E8, 0x00E9)  # + sheep, cow
    # else: # above 80
        return (0x00E8, 0x00E9)  # + bull

def move_to_target(target):
    if GetDistance(target) > 1:
        NewMoveXY(GetX(target), GetY(target), True, 1, True)

def check_journal(start_time, messages):
    return InJournalBetweenTimes("|".join(messages), start_time, datetime.now()) > 0

def attempt_taming(target):
    start_time = datetime.now()
    UseSkill('Animal taming')
    WaitTargetObject(target)
    print(f"taming {target}")

    end_time = start_time + timedelta(seconds=TAMING_TIMEOUT)
    while datetime.now() < end_time:
        if check_journal(start_time, ["had too many"]):
            print("TOO MANY FOLLOWERS, KILLING ANIMAL")
            if kill_animal(target):
                return False
        if check_journal(start_time, ["accept you", "looks tame", "even challenging."]):
            print("RETURNED TRUE")
            return True
        if check_journal(start_time, ["Someone else is already taming", "cannot be"]):
            print("RETURNED FALSE")
            return False
        if check_journal(start_time, ["fail to", "clear path", "is too far"]):
            print("RETRY")
            return None  # Return None to indicate a retry is needed

        move_to_target(target)

    return IsObjectExists(target) and GetHP(target) > 0

def kill_animal(target):
    end_time = datetime.now() + timedelta(seconds=30)  # 30 seconds timeout
    while IsObjectExists(target) and GetHP(target) > 0 and datetime.now() < end_time:
        Attack(target)
        Wait(1000)
    return not IsObjectExists(target) or GetHP(target) == 0

def release_pet(target):
    end_time = datetime.now() + timedelta(seconds=RELEASE_TIMEOUT)
    while IsObjectExists(target) > 0 and PetsCurrent() > 0 and datetime.now() < end_time:
        Attack(target)
        Wait(1000)
        if not IsObjectExists(target):
            return True
        # UOSay(f"{GetName(target)} release")
        # Wait(1000)
        # if wait_for_gump(RELEASE_GUMP, RELEASE_BUTTON):
        #     Wait(1000)
        #     if not IsObjectExists(target):
        #         return True

    return False

def tame_target(target):
    while IsObjectExists(target) > 0 and PetsCurrent() < MAX_PETS and GetHP(target) > 0:
        move_to_target(target)

        taming_result = attempt_taming(target)
        if taming_result is False:
            return False
        elif taming_result is True:
            if not release_pet(target):
                print(f"Failed to release pet {target}, ignoring")
                return False
            return True
        # If taming_result is None, continue the loop to retry

    return False

def tame_all_at_location():
    skill = GetSkillValue('Animal taming')
    animals = get_animals_by_skill(skill)

    found_animals = True
    while found_animals:
        found_animals = False
        for animal in animals:
            while FindType(animal, Ground()) > 0:
                found_animals = True
                targets = sorted(GetFindedList(), reverse=True, key=GetDistance)
                for target in targets:
                    tame_target(target)
                    if PetsCurrent() >= MAX_PETS:
                        return

def main():
    SetFindDistance(40)
    SetFindVertical(40)
    rail = [
        #(5140, 3964),
        (5167, 3981),
        #(5193, 4017),
        #(5223, 4032),
        #(5225, 3977),
        #(5209, 3956),
    ]  # Add more coordinates as needed

    while GetSkillValue('Animal taming') < TARGET_SKILL:
        for x, y in rail:
            NewMoveXY(x, y, True, 2, True)
            tame_all_at_location()

if __name__ == "__main__":
    main()
