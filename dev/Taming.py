from datetime import datetime, timedelta
from py_stealth import *


def tame():
    animals = (0x00DC, 0x00D8, 0x00ED, 0x00CD, 0x00CF, 0x0006)
    for animal in animals:
        if FindType(animal, Ground()) > 0:
            mobarounds = GetFindedList()
            mobarounds.sort(reverse=True, key=GetDistance)
            for target in mobarounds:
                while IsObjectExists(target) > 0 and PetsCurrent() < 5 and GetHP(target) > 0:
                    if GetDistance(target) > 1:
                        NewMoveXY(GetX(target), GetY(target), True, 1, True)
                    timeout = datetime.now() + timedelta(milliseconds=25000)
                    starttime = datetime.now()
                    UseSkill('Animal taming')
                    WaitTargetObject(target)
                    tamed = False
                    while not tamed:
                        if ((InJournalBetweenTimes("accept you ", starttime, datetime.now())) > 0):
                            tamed = True
                        elif ((InJournalBetweenTimes("fail to ", starttime, datetime.now())) > 0):
                            starttime = datetime.now()
                            timeout = datetime.now() + timedelta(milliseconds=25000)
                            UseSkill('Animal taming')
                            WaitTargetObject(target)
                        elif datetime.now() > timeout:
                            return
                        if GetDistance(target) > 1:
                            NewMoveXY(GetX(target), GetY(target), True, 1, True)
                        Wait(50)
                    timeout = datetime.now() + timedelta(milliseconds=25000)
                    while IsObjectExists(target) > 0:
                        if GetDistance(target) > 1:
                            NewMoveXY(GetX(target), GetY(target), True, 1, True)
                        Attack(target)
                        Wait(50)
                        if datetime.now() > timeout:
                            return


SetFindDistance(40)
SetFindVertical(40)
rail = [(2118, 2795), (2115, 2778), (2113, 2745), (2113, 2709), (2103, 2685), (2083, 2661)]
while GetSkillValue('Animal taming') < 100.0:
    for x, y in rail:
        NewMoveXY(x, y, True, 1, True)
        tame()