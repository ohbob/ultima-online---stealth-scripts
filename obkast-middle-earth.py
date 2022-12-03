# ======================================================================
# Script Name: Obkast
# Author: CAMOTbIK
# Version: 0.1 Beta
# Shard OSI / FS:  FS Middle Earth
# Revision Date: 2022/12/01
# Public Release: 2022/12/01
# Global Variables Used: None
# Purpose: Cast buffs on targets
# ======================================================================

from py_stealth import *
import time

phrase = "obk"
storage = 0x678DE9F9
food = 0x171F
foodtimer = time.time()


def TypeQuantity(type, color=0x0000, container=Backpack()):
    FindTypeEx(type, color, container, True)
    return FindFullQuantity()


def restock():
    UseObject(storage)
    CheckLag(1500)
    items = [GA(), SA(), NS(), SS(), BM(), MR(), NS(), food]
    for item in items:
        amount = TypeQuantity(item)
        if amount <= 3:  # if found less than n regs
            if FindTypeEx(item, 0x0000, storage) > 0:  # if found the reg in storage
                MoveItem(FindItem(), 10 - amount, Backpack(), 0, 0, 0)
                Wait(500)


def meditate():
    while Mana() < MaxMana():
        UseSkill("Meditation")
        Wait(5000)


def eat():
    global foodtimer
    if time.time() > foodtimer + 60:
        # update the new value
        foodtimer = time.time()
        UseType2(food)


index = HighJournal()
while True:
    while index < HighJournal():
        index = index + 1
        line = Journal(index)
        # print(f"sender ID: {LineID()} - {line}")  # do whatever you need to do here
        if phrase in line:
            target = LineID()
            if CheckLOS(GetX(Self()), GetY(Self()), GetZ(Self()), GetX(target), GetY(target), GetZ(target), WorldNum(),
                        4):
                UOSay(".cast dayofgods")
                Wait(2500)
                UOSay(".cast cprotpoison")
                WaitTargetObject(target)
                Wait(2500)
                CastToObject('Bless', target)
                Wait(2500)
                CastToObject('Protection', target)
                Wait(2500)
                restock()
                meditate()
            else:
                UOSay("Тебя не видно! Подойди по ближе")
                Wait(1000)

        while Dead():
            Wait(1000)
    eat()
    Wait(100)
