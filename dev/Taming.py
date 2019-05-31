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


def tame():
    skill = GetSkillValue('Animal taming')
    if skill < 30:
        animals = (0x00CD, 0x0006) # rabbit, birds
    if skill > 30:
        animals = (0x00CD, 0x0006, 0x00CF, 0x00D8, 0x00E7) # rabbit, birds, sheep, cow
    if skill > 50:
        animals = (0x00CD, 0x0006, 0x00CF, 0x00D8, 0x00E7, 0x00ED)  # rabbit, birds, sheep, cow, hind
    if skill > 50:
        animals = (0x00CD, 0x0006, 0x00CF, 0x00D8, 0x00E7, 0x00ED, 0x00DC)  # rabbit, birds, sheep, cow, hind, llama
    if skill > 70:
        animals = (0x00CD, 0x0006, 0x00CF, 0x00D8, 0x00E7, 0x00ED, 0x00DC, 0x00EA) # rabbit, birds, sheep, cow, hind, llama, great hart
    if skill > 80:
        animals = (0x00CD, 0x0006, 0x00CF, 0x00D8, 0x00E7, 0x00ED, 0x00DC, 0x00EA, 0x00E8, 0x00E9) # rabbit, birds, sheep, cow, hind, llama, great hart, a bull

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
                        elif ((InJournalBetweenTimes("fail to |clear path |", starttime, datetime.now())) > 0):
                            starttime = datetime.now()
                            timeout = datetime.now() + timedelta(milliseconds=25000)
                            UseSkill('Animal taming')
                            WaitTargetObject(target)
                        elif ((InJournalBetweenTimes("Someone else is already taming |cannot be |too far", starttime, datetime.now())) > 0):
                            return
                        elif ((InJournalBetweenTimes("looks tame ", starttime, datetime.now())) > 0):
                            Ignore(target)
                            return
                        elif datetime.now() > timeout:
                            return
                        if GetDistance(target) > 1:
                            NewMoveXY(GetX(target), GetY(target), True, 1, True)
                        Wait(50)
                    if GetSkillValue('Swordsmanship') < 100.0:
                        UseType2(0x13F6)  # butchers knife
                    elif GetSkillValue('Fencing') < 100.0:
                        UseType2(0x0F52)  # dagger
                    elif GetSkillValue('Mace fighting') < 100.0:
                        UseType2(0x13B4)  # Club
                    timeout = datetime.now() + timedelta(milliseconds=25000)
                    while IsObjectExists(target) > 0:
                        if GetDistance(target) > 1:
                            NewMoveXY(GetX(target), GetY(target), True, 1, True)
                        Attack(target)
                        if TargetPresent():
                            CancelTarget()
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
