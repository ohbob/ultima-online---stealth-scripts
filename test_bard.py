from py_stealth import *
import time
import datetime

SetFindDistance(12)
debugging = True
delay_blade_spirits = 1
delay_discordance = 1
delay_dispel = 1
delay_between_skills = 1
timer_blade_spirits = time.time()
timer_discordance = time.time()
timer_dispel = time.time()
timer_between_skills = time.time()

def debug(message, color):
    if debugging:
        ClientPrintEx(Self(), color, 0, message)
        AddToSystemJournal(message)

def update_delays(blade_spirits=None, discordance=None, dispel=None, between_skills=None):
    global delay_blade_spirits, delay_discordance, delay_dispel, delay_between_skills
    if blade_spirits is not None:
        delay_blade_spirits = blade_spirits
    if discordance is not None:
        delay_discordance = discordance
    if dispel is not None:
        delay_dispel = dispel
    if between_skills is not None:
        delay_between_skills = between_skills
    debug(f"Delays updated: Blade Spirits={delay_blade_spirits}, Discordance={delay_discordance}, Dispel={delay_dispel}, Between Skills={delay_between_skills}", 90)

def cast_blade_spirits():
    global timer_blade_spirits, timer_between_skills
    if (time.time() - timer_blade_spirits >= delay_blade_spirits and
        time.time() - timer_between_skills >= delay_between_skills):
        debug("Casting Blade Spirits...", 22)
        Cast('Blade Spirit')
        WaitTargetObject(0x417C76CF)
        Wait(1000)
        if FindTypesArrayEx([0x023E], [0xffff], [Ground()], False):
            debug("Blade Spirits cast successfully", 25)
            timer_blade_spirits = time.time()
            timer_between_skills = time.time()
            return True
        else:
            debug("Blade Spirits failed: Not found after casting", 31)
    return False

def use_discordance(target):
    global timer_discordance, timer_between_skills
    if (GetSkillValue('Discordance') > 40.9 and
        FindTypesArrayEx([0x0EB3], [0xFFFF], [Backpack()], True) != 0 and
        time.time() - timer_discordance >= delay_discordance and
        time.time() - timer_between_skills >= delay_between_skills):
        
        if TargetPresent():
            CancelTarget()
        
        start_time = datetime.datetime.now()
        UseSkill('Discordance')
        WaitForTarget(1000)
        debug('Attempting Discordance...', 22)
        
        if TargetPresent():
            TargetToObject(target)
            Wait(500)
        
        if InJournalBetweenTimes('You play successfully', start_time, datetime.datetime.now()) != -1:
            debug('Discordance successful', 25)
            timer_discordance = time.time()
            timer_between_skills = time.time()
            return True
        elif InJournalBetweenTimes('but fail', start_time, datetime.datetime.now()) != -1:
            debug('Discordance failed', 31)
            timer_between_skills = time.time()
        elif InJournalBetweenTimes('too far away', start_time, datetime.datetime.now()) != -1:
            debug('Target too far away for Discordance', 31)
        elif InJournalBetweenTimes('already under the effect', start_time, datetime.datetime.now()) != -1:
            debug('Target already discorded', 90)
            return True
        else:
            debug('Discordance attempt inconclusive', 31)
    else:
        debug('Discordance conditions not met', 90)
    
    return False

def cast_dispel(target):
    global timer_dispel, timer_between_skills
    if (time.time() - timer_dispel >= delay_dispel and
        time.time() - timer_between_skills >= delay_between_skills):
        debug("Casting Dispel...", 22)
        Cast('Dispel')
        WaitForTarget(1000)
        if TargetPresent():
            TargetToObject(target)
            Wait(500)
        start_time = datetime.datetime.now()
        if InJournalBetweenTimes('The magic is dispelled', start_time, datetime.datetime.now()) != -1:
            debug("Dispel successful", 25)
            timer_dispel = time.time()
            timer_between_skills = time.time()
            return True
        else:
            debug("Dispel failed or inconclusive", 31)
    return False

def main():
    debug("Starting Blade Spirits, Discordance, and Dispel loop...", 90)
    
    while not Dead():
        FindType(0x023E, Ground())
        blade_spirit = FindItem()
        
        if not blade_spirit:
            debug("No Blade Spirit found, attempting to cast...", 25)
            success = cast_blade_spirits()
            if not success:
                debug("Failed to cast Blade Spirits", 31)
            Wait(1000)
        else:
            debug("Blade Spirit found, attempting Discordance", 25)
            success = use_discordance(blade_spirit)
            if success:
                debug("Discordance successful or already applied, casting Dispel", 25)
                dispel_success = cast_dispel(blade_spirit)
                if not dispel_success:
                    debug("Dispel attempt unsuccessful", 31)
            else:
                debug("Discordance attempt unsuccessful", 31)
            
            # Check if Blade Spirit is still present after actions
            FindType(0x023E, Ground())
            if not FindItem():
                debug("Blade Spirit disappeared, will cast a new one in the next iteration", 25)
        
        Wait(1000)

    while Dead():
        Wait(5000)

if __name__ == "__main__":
    main()

# Example of how to update delays:
# update_delays(blade_spirits=45, discordance=40, dispel=30, between_skills=10)