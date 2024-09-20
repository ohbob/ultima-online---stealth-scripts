from py_stealth import *
import datetime


SKILL_SPELL_MAPPING = {
    'Magery': [
        {'max_skill': 89.0, 'spell': 'Blade Spirit', 'creature_type': 0x023E, 'wait_time': 1000},
        {'max_skill': 90.0, 'spell': 'Energy Vortex', 'creature_type': 0x00A4, 'wait_time': 2000},
        {'max_skill': 94.1, 'spell': 'summon water elemental', 'creature_type': 0x0010, 'wait_time': 3500},
        {'max_skill': 97.7, 'spell': 'animal', 'creature_type': 0x000F, 'wait_time': 3500},
    ]
}

ANIMAL_MAPPING = {
    'Discordance': [
        {'max_skill' : 106.5, 'creature_type' : 0x0115},
        {'max_skill' : 120, 'creature_type' : 0x000C},
    ]
}

MESSAGES = {
    'discordance_success': 'You play jarring music',
    'discordance_already': 'is already',
    'discordance_fail': 'but fail',
    'discordance_far': 'That is too far away',
    'need_instrument': 'What instrument',
    'spell_fail': 'The spell fizzles',
}

SetFindDistance(12)

instrument_type = 0x0EB3
item_to_cast_to = 0x417C76CF
debugging = True

def debug(message, color):
    if debugging:
        ClientPrintEx(Self(), color, 0, message)
        print(message)


def cast_summoned_creature():
    magery_skill = GetSkillValue('Magery')
    spell_info = next((info for info in SKILL_SPELL_MAPPING['Magery'] if magery_skill < info['max_skill']), None)
    
    if not spell_info:
        debug(f"No suitable spell found for Magery skill {magery_skill}", 31)
        return False

    debug(f"Casting {spell_info['spell']}...", 22)
    start_time = datetime.datetime.now()
    Cast(spell_info['spell'])
    WaitJournalLine(start_time, MESSAGES['spell_fail'], spell_info['wait_time'])
    # Wait(spell_info['wait_time'])
    WaitTargetObject(item_to_cast_to)
    # Wait(500)  # Reduced wait time after casting
    if FindTypesArrayEx([spell_info['creature_type']], [0xffff], [Ground()], False):
        UOSay("All guard me")
        debug(f"{spell_info['spell']} cast successfully", 25)
        return True
    else:
        debug(f"{spell_info['spell']} failed: Not found after casting", 31)
    return False

def meditate():
    if GetMana(Self()) < 40 and GetSkillValue('Meditation') > 0:
        debug("Mana low, attempting to meditate...", 22)
        while GetMana(Self()) != MaxMana():
            UseSkill('Meditation')
            Wait(11000)  # Wait for 11 seconds
        if GetMana(Self()) > GetMaxMana(Self()) * 0.9:
            debug("Meditation successful", 25)
            return True
        else:
            debug("Meditation incomplete", 31)
    return False

def use_discordance(target):
    if GetSkillValue('Discordance') > 40.9:
        if TargetPresent():
            CancelTarget()
        
        start_time = datetime.datetime.now()
        UseSkill('Discordance')
        WaitForTarget(1000)
        
        if InJournalBetweenTimes(MESSAGES['need_instrument'], start_time, datetime.datetime.now()) > 0:
            debug('Need to target an instrument', 22)
            instrument = FindType(instrument_type, Backpack())
            if instrument == 0:
                debug('No musical instrument found in backpack', 31)
                return exit()
            if TargetPresent():
                TargetToObject(instrument)
                WaitForTarget(1000)

        if TargetPresent():
            debug('Targeting creature for Discordance...', 22)
            TargetToObject(target)
            WaitJournalLine(start_time, f"{MESSAGES['discordance_success']}|{MESSAGES['discordance_already']}|{MESSAGES['discordance_fail']}|{MESSAGES['discordance_far']}|{MESSAGES['need_instrument']}", 7000)            
            if InJournalBetweenTimes(MESSAGES['discordance_success'], start_time, datetime.datetime.now()) > 0 or InJournalBetweenTimes(MESSAGES['discordance_already'], start_time, datetime.datetime.now()) > 0:
                debug('Discordance successful or already applied', 25)
                return True
            elif InJournalBetweenTimes(MESSAGES['discordance_fail'], start_time, datetime.datetime.now()) > 0:
                debug('Discordance failed', 31)
            elif InJournalBetweenTimes(MESSAGES['discordance_far'], start_time, datetime.datetime.now()) > 0:
                debug('Target too far away for Discordance', 31)
            else:
                debug('Discordance attempt inconclusive', 31)
        else:
            debug('Failed to get target for Discordance', 31)
    else:
        debug('Discordance skill too low or conditions not met', 90)
    
    return False

def release_creature(target):
    creature_name = GetName(target)
    debug(f"Attempting to release {creature_name}...", 22)
    UOSay(f"{creature_name} release")

    if not IsObjectExists(target):
        debug(f"Successfully released {creature_name}", 25)
        return True
    else:
        debug(f"Failed to release {creature_name}", 31)
        return False

def find_creature_for_discordance():
    discordance_skill = GetSkillValue('Discordance')
    creature_info = next((info for info in ANIMAL_MAPPING['Discordance'] if discordance_skill < info['max_skill']), None)
    
    if not creature_info:
        return None

    FindType(creature_info['creature_type'], Ground())
    return FindItem()

def use_hiding():
    while not Hidden():
        debug("Using Hiding skill...", 22)
        UseSkill('Hiding')
        Wait(1000)  # Short wait to allow hiding to take effect

def main():
    debug("Starting Discordance training loop...", 90)
    
    while not Dead():
        if GetMana(Self()) < 40:
            meditate()
            continue

        discordance_skill = GetSkillValue('Discordance')
        
        if discordance_skill < 97.7:
            # Original logic for training on summoned creatures
            magery_skill = GetSkillValue('Magery')
            spell_info = next((info for info in SKILL_SPELL_MAPPING['Magery'] if magery_skill < info['max_skill']), None)
            
            if not spell_info:
                debug(f"No suitable spell found for Magery skill {magery_skill}", 31)
                continue

            FindType(spell_info['creature_type'], Ground())
            summoned_creature = FindItem()
            
            if not summoned_creature:
                debug(f"No {spell_info['spell']} found, attempting to cast...", 25)
                success = cast_summoned_creature()
                if not success:
                    debug(f"Failed to cast {spell_info['spell']}", 31)
            else:
                debug(f"{spell_info['spell']} found, attempting Discordance", 25)
                success = use_discordance(summoned_creature)
                if success:
                    debug("Discordance successful or already applied, releasing creature", 25)
                    release_creature(summoned_creature)
                else:
                    debug("Discordance attempt unsuccessful", 31)
                
                FindType(spell_info['creature_type'], Ground())
                if not FindItem():
                    debug(f"{spell_info['spell']} disappeared, will cast a new one in the next iteration", 25)
        else:
            # New logic for training on real creatures
            target = find_creature_for_discordance()
            if target:
                success = use_discordance(target)
                if success:
                    debug("Discordance successful, using Hiding and waiting", 25)
                    use_hiding()
                    Wait(15000)  # Wait for 17 seconds
                else:
                    debug("Discordance attempt unsuccessful", 31)
            else:
                debug("No suitable creature found for Discordance training", 31)
                Wait(5000)  # Wait before trying again

    while Dead():
        Wait(5000)

if __name__ == "__main__":
    main()

