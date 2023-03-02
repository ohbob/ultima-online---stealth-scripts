from py_stealth import *

throw = [0x09D0, 0x097B, 0x09D1, 0x097D, 0x09D2]
keep = [0x09B7, 0x09EB, 0x09F2, 0x09C0, 0x09D3]
box = 0x450F0226
trash = 0x45C4076C
casttime = 1500
medittime = 5000

while True:
    
    while not Connected():
        Wait(60000)
        Connect()

    while Connected() and not Dead():
        for itemType in throw:
            MoveItems(Backpack(), itemType, 0xFFFF, trash, 0, 0, 0, 500, 0)
        for itemType in keep:
            MoveItems(Backpack(), itemType, 0xFFFF, box, 0, 0, 0, 500, 0)

        for i in range(1, 200):
            if Mana() > 4:
                Cast("Create food")
                Wait(casttime)
            else:
                while Mana() != MaxMana():
                    UseSkill('Meditation')
                    Wait(medittime)
                    
    if Connected() and Dead():
        break
