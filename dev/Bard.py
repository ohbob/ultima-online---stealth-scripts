from py_stealth import *
import time
import datetime

debugging = True
delaypeacemaking = 30
delaydiscordance = 30
delaybetweenbard = 5
timerpeace = time.time()
timerdiscordance = time.time()
timerbetweenbard = time.time()



def debug(message, color):
    if debugging:
        ClientPrintEx(Self(), color, 0, message)
        AddToSystemJournal(message)


def search_target():
    SetFindDistance(20)
    if FindTypesArrayEx([0x00DD], [0xffff], [Ground()], False):
        debug('found a mob', 31)
        return True
    # else:
    #     debug('found nothing', 22)


def kill(target):
    while IsObjectExists(target):
        # Attack(target)
        if GetDistance(target) < 13:
            peacemaking(target)
            discordance(target)
        if GetDistance(target) > 2:
            debug('moving closer', 15)
            NewMoveXY(GetX(target), GetY(target), True, 1, True)
        Wait(100)


def peacemaking(target):
    global timerpeace
    global timerbetweenbard
    global delaypeacemaking
    global delaybetweenbard
    if (GetSkillValue('Peacemaking') > 49.9) \
            and (FindTypesArrayEx([0x0E9C], [0xFFFF], [Backpack()], True) != 0) \
            and timerpeace + delaypeacemaking > time.time() \
            and timerbetweenbard + delaybetweenbard > time.time():
        if TargetPresent():
            CancelTarget()
        starttime = datetime.datetime.now()
        UseSkill('Peacemaking')
        WaitForTarget(2000)
        debug('Using Peacemaking', 22)
        Wait(1000)
        if InJournalBetweenTimes('What instrument shall you play?', starttime, datetime.datetime.now() > 0):
            WaitTargetObject(FindItem())
            debug('Added new instrument', 25)
            UseSkill('Peacemaking')
            WaitForTarget(2000)
        if TargetPresent():
            TargetToObject(target)
            WaitJournalLine(datetime.datetime.now(), ' You play successfully |You fail to pacify |too far away ', 1000)
        if InJournalBetweenTimes('You play successfully', starttime, datetime.datetime.now()):
            debug('successfully', 25)
            timerpeace = time.time()
            timerbetweenbard = time.time()
        if InJournalBetweenTimes('You fail to pacify', starttime, datetime.datetime.now()):
            debug('failed', 31)
            timerbetweenbard = time.time()


def discordance(target):
    global timerdiscordance
    global timerbetweenbard
    global delaydiscordance
    global delaybetweenbard
    if (GetSkillValue('Discordance') > 49.9) \
            and (FindTypesArrayEx([0x0E9C], [0xFFFF], [Backpack()], True) != 0) \
            and timerdiscordance + delaydiscordance > time.time() \
            and timerbetweenbard + delaybetweenbard > time.time():
        if TargetPresent():
            CancelTarget()
        starttime = datetime.datetime.now()
        UseSkill('Discordance')
        WaitForTarget(2000)
        debug('Using Discordance', 22)
        Wait(1000)
        if InJournalBetweenTimes('What instrument shall you play?', starttime, datetime.datetime.now()):
            WaitTargetObject(FindItem())
            debug('Added new instrument', 25)
            UseSkill('Discordance')
            WaitForTarget(2000)
        if TargetPresent():
            TargetToObject(target)
            WaitJournalLine(datetime.datetime.now(), ' You play successfully |You fail to discord |too far away ', 1000)
        if InJournalBetweenTimes('You play successfully', starttime, datetime.datetime.now()):
            debug('successfully', 25)
            timerpeace = time.time()
            timerbetweenbard = time.time()
        if InJournalBetweenTimes('You fail to discord', starttime, datetime.datetime.now()):
            debug('failed', 31)
            timerbetweenbard = time.time()


# mainloop
def main():
    while True:
        while not Dead():

            if search_target():
                current = FindItem()
                kill(current)

                # cut()
                # loot()

            # if over_weight():
            #     travel(home)
            #     unload()
            #     upload()
            #     travel(farm)

        while Dead():
            Wait(50000)
        Wait(100)


# mainloop end

if __name__ == "__main__":
    main()
