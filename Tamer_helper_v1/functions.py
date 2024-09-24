from py_stealth import *
import time
import datetime
from damage_counter import *

discord_cooldowns = {}
last_discord_use = 0

def buff_exists(name):
    if not name:
        return False
    for buff in GetBuffBarInfo():
        buff_name = GetClilocByID(buff['ClilocID1']).upper()
        if name.upper() in buff_name:
            return True
    return False

def buffs_exist(names):
    if not names:
        return False
    for buff in GetBuffBarInfo():
        buff_name = GetClilocByID(buff['ClilocID1']).upper()
        for name in names:
            if name.upper() in buff_name:
                return True
    return False

def BANDAGE(id, threshold):
    if (GetSkillValue("Healing") > 50 or GetSkillValue("Veterinary") > 50) and not buffs_exist(['Veterinary', 'Healing']): 
        if GetDistance(id) < 3:
            if UseType2(0x0E21):
                WaitForTarget(500)
                if TargetPresent:
                    TargetToObject(id)
                    # Wait(500)

def Veterinary(id, threshold):
    if GetSkillValue("Veterinary") > 50 and not buffs_exist(['Veterinary', 'Healing']) and GetDistance(id) < 3:
        if UseType2(0x0E21):
            WaitForTarget(500)
            if TargetPresent:
                TargetToObject(id)
                # Wait(500)

def Heal(target, threshold):
    if GetHP(target) < threshold:
        if GetSkillValue("Magery") > 50 and Mana() > 10:
            Cast("Greater Heal")
        elif GetSkillValue("Chivalry") > 50 and Mana() > 10:
            Cast("Close Wounds")
        else:
            return
        WaitForTarget(2000)
        if TargetPresent():
            TargetToObject(target)

def EB():
    if GetSkillValue("Magery") > 50:
        AddToSystemJournal("War target", WarTargetID())
        if Mana() > 15 and WarTargetID() != 0:
            Cast("Energy bolt")
            WaitForTarget(3500)
            if TargetPresent() and GetHP(WarTargetID()) > 0:
                TargetToObject(WarTargetID())

def FS():
    print("FS function called")  # Debug log
    if GetSkillValue("Magery") > 50:
        print(f"Magery skill: {GetSkillValue('Magery')}")  # Debug log
        AddToSystemJournal("War target", WarTargetID())
        if Mana() > 20 and WarTargetID() != 0:
            print(f"Mana: {Mana()}, WarTargetID: {WarTargetID()}")  # Debug log
            Cast("Flame Strike")
            WaitForTarget(3500)
            if TargetPresent() and GetHP(WarTargetID()) > 0:
                print("Targeting war target")  # Debug log
                TargetToObject(WarTargetID())
            else:
                print("No valid target for Flame Strike")  # Debug log
        else:
            print("Not enough mana or no war target")  # Debug log
    else:
        print("Magery skill too low for Flame Strike")  # Debug log

def MORTAL(target):
    if GetSkillValue("Chivalry") > 50 and IsYellowHits(target) and Mana() > 15:
        Cast("Remove Curse")
        WaitForTarget(2500)
        if TargetPresent() and IsYellowHits(target):
            TargetToObject(target)
            Wait(500)
        else:
            if TargetPresent():
                CancelTarget()

def CURE(target, threshold):
    if IsPoisoned(target) and Mana() > 15:
        if GetSkillValue("Magery") > 50:
            Cast("Cure")
        elif GetSkillValue("Chivalry") > 50:
            Cast("Cleanse by fire")
        else:
            return
        WaitForTarget(2500)
        if TargetPresent() and IsPoisoned(target):
            TargetToObject(target)
            Wait(500)
        else:
            if TargetPresent():
                CancelTarget()

def follow(id, distance):
    if id_distance := GetDistance(id) > distance:
        print(f"Following {id} at {id_distance} tiles")
        NewMoveXY(GetX(id), GetY(id), True, distance, True)

def discord(friendlist=[], petlist=[]):
    if GetSkillValue("Discordance") > 40 and GetSkillValue("Musicianship") > 40:
        global last_discord_use
        current_time = time.time()
        
        # Check if 7 seconds have passed since the last Discordance use
        if current_time - last_discord_use < 3:
            print(f"Discordance on global cooldown. Waiting...")
            return

        FindTypesArrayEx([0xFFFF], [0xFFFF], [Ground()], False)
        targets = [t for t in GetFindedList() if 3 < GetNotoriety(t) < 7 
                   and t not in friendlist
                   and t not in petlist 
                   and t != Self()]
        targets.sort(key=lambda t: GetDistance(t))
        
        for target in targets:
            # Check if the target is on cooldown
            if target in discord_cooldowns and current_time - discord_cooldowns[target] < 30:
                print(f"Skipping target (ID: {target}) - on Discord cooldown")
                continue

            distance = GetDistance(target)
            # print(f"Checking target (ID: {target}), distance: {distance}")
            
            if distance <= 12:
                print(f"Attempting to use Discord on target (ID: {target}) {GetName(target)}")
                if use_discordance(target):
                    discord_cooldowns[target] = current_time
                    last_discord_use = current_time
                    print(f"Discord successful on target (ID: {target}). Cooldowns started.")
                    return
            else:
                print(f"Target (ID: {target}) is too far for Discord.")

def use_discordance(target):
    instrument_type = 0x0EB3
    MESSAGES = {
    'discordance_success': 'You play jarring music',
    'discordance_already': 'is already',
    'discordance_fail': 'but fail',
    'discordance_far': 'That is too far away',
    'need_instrument': 'What instrument',
}
    
    # if GetSkillValue('Discordance') > 40.9:
    if TargetPresent():
        CancelTarget()
    
    start_time = datetime.datetime.now()
    UseSkill('Discordance')
    WaitForTarget(1000)
    
    if InJournalBetweenTimes(MESSAGES['need_instrument'], start_time, datetime.datetime.now()) > 0:
        print('Need to target an instrument')
        instrument = FindType(instrument_type, Backpack())
        if instrument == 0:
            print('No musical instrument found in backpack')
            return False
        if TargetPresent():
            TargetToObject(instrument)
            WaitForTarget(1000)

    if TargetPresent():
        print('Targeting creature for Discordance...')
        TargetToObject(target)
        WaitJournalLine(start_time, f"{MESSAGES['discordance_success']}|{MESSAGES['discordance_already']}|{MESSAGES['discordance_fail']}|{MESSAGES['discordance_far']}|{MESSAGES['need_instrument']}", 7000)            
        if InJournalBetweenTimes(MESSAGES['discordance_success'], start_time, datetime.datetime.now()) > 0 or InJournalBetweenTimes(MESSAGES['discordance_already'], start_time, datetime.datetime.now()) > 0:
            print('Discordance successful or already applied')
            return True
        elif InJournalBetweenTimes(MESSAGES['discordance_fail'], start_time, datetime.datetime.now()) > 0:
            print('Discordance failed')
        elif InJournalBetweenTimes(MESSAGES['discordance_far'], start_time, datetime.datetime.now()) > 0:
            print('Target too far away for Discordance')
        else:
            print('Discordance attempt inconclusive')
    # else:
    #     print('Discordance skill too low or conditions not met')
    
    return False


from py_stealth import *
def CW():
    if GetSkillValue("Chivalry") > 50 and Mana() > 10 and buff_exists("Enemy of One") and not buff_exists("Consecrate") and WarTargetID() > 0:
        Cast("Consecrate Weapon")
        Wait(50)

def DF():
    if GetSkillValue("Chivalry") > 50 and Mana() > 10 and not buff_exists("Divine Fury") and buff_exists("Enemy of One") and WarTargetID() > 0:
        Cast("Divine Fury")


def PRI():
    if GetSkillValue("Tactics") > 80:
        active_ability = GetActiveAbility()
        if Mana() > 25 and (active_ability == 0 or active_ability == "0"):
            print("Activating primary")
            UsePrimaryAbility()

def SEC():
    if GetSkillValue("Tactics") > 80:
        if Mana() > 25 and GetActiveAbility() == 0:
            print("Activating secondary")
            UseSecondaryAbility()
        print("SEC function called")

def EOO():
    if GetSkillValue("Chivalry") > 50 and Mana() > 15 and not buff_exists("Enemy of One"):
        Cast("Enemy of One")

def LS():
    if GetSkillValue("Bushido") > 50 and Mana() > 10 and not IsActiveSpellAbility('lightning strike'):
        Cast("Lightning Strike")
        Wait(100)


honored = {}
honor_cooldowns = {}
last_honor_use = 0

def HONOR(friendlist=[], petlist=[]):
    if GetSkillValue("Bushido") > 50:
        global last_honor_use
        current_time = time.time()

        # Check if 3 seconds have passed since the last Honor use
        if current_time - last_honor_use < 3:
            print(f"Honor on global cooldown. Waiting...")
            return

        FindTypesArrayEx([0xFFFF], [0xFFFF], [Ground()], False)
        targets = [t for t in GetFindedList() if 2 < GetNotoriety(t) < 7
                   and t not in friendlist
                   and t not in petlist
                   and t != Self()
                   and t not in honored]  # Add this condition
        
        targets.sort(key=lambda t: GetDistance(t))

        for target in targets:
            # Check if the target is on cooldown
            if target in honor_cooldowns and current_time - honor_cooldowns[target] < 30:
                print(f"Skipping target (ID: {target}) - on Honor cooldown")
                continue

            distance = GetDistance(target)
            if distance <= 10 and GetHP(target) == 25:
                print(f"Attempting to use Honor on target (ID: {target}) {GetName(target)}")
                if use_honor(target):
                    honor_cooldowns[target] = current_time
                    last_honor_use = current_time
                    honored[target] = True  # Add this line
                    print(f"Honor successful on target (ID: {target}). Cooldowns started.")
                    return
                else:
                    print(f"Failed to honor target (ID: {target})")
            else:
                print(f"Target (ID: {target}) is too far or has low HP for Honor.")

def use_honor(target):
    if TargetPresent():
        CancelTarget()

    # ReqVirtuesGump()
    # WaitForTarget(2500)
    UseVirtue('honor')
    WaitForTarget(3000)
    TargetToObject(target)
    Wait(50)

    before = datetime.datetime.now()
    # Check if honor was successful
    if InJournalBetweenTimes("You have honored your opponent", before, datetime.datetime.now()) > 0:
        honored[target] = True
        # ClientPrint()
        ClientPrintEx(Self(), 1, 1, f"* Honored {GetName(target)} *")
        # print(f"Successfully honored target {target}")
        return True
    else:
        print(f"Failed to honor target {target}")
        return False

print("HONOR function called")

# Add this function to integrate damage counter with the main loop
def update_damage_counter():
    pass
    # if WarTargetID() == 0 and damage_counter['enemy'] != 0 and not IsObjectExists(damage_counter['enemy']):
        # reset_and_print_stats()

# Modify the existing SetEventProc call to include the damage function
SetEventProc('evwardamage', damage)