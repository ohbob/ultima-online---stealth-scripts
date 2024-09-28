from py_stealth import *
from datetime import datetime




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


# print(buff_exists_('Nature\'s Fury'))

# buffs = GetBuffBarInfo()
# # print(buffs)
# for i in buffs:
#     print(i)
#     print(GetClilocByID(i['ClilocID1']))
# #     # print(GetClilocByID(i['ClilocID2']))


# print(buffs_exist(['Veterinary', 'Healing']))


# {'Attribute_ID': 1069, 'TimeStart': datetime.datetime(2024, 9, 19, 2, 17, 54, 400000), 'Seconds': 4, 'ClilocID1': 1002082, 'ClilocID2': 1151400}

# while True:
#     if Mana() > 20:
#         Cast("Noble Sacrifice")
#         Wait(1000)

def deconstruct_gump():
    for i in range(GetGumpsCount()):
        gump = GetGumpInfo(i)
        for entry in gump:
            print(f"---------\n"
                  f"{entry}")
            if len(entry) > 0:
                subentries = gump[entry]
                if type(subentries) == list:
                    for x in subentries:
                        print(x)
                else:
                    print(subentries)

deconstruct_gump()

def waitgumpid_press(gumpid, number=0, pressbutton=True, timeout=15):
    maxcounter = 0
    while maxcounter < timeout * 10:
        if IsGump():
            for currentgumpnumb in range(0, (GetGumpsCount())):
                currentgump = GetGumpInfo(currentgumpnumb)
                if 'GumpID' in currentgump:  # got to check if key exists or we might get an error
                    if currentgump['GumpID'] == gumpid:
                        if pressbutton:
                            NumGumpButton(currentgumpnumb, number)
                        else:
                            return currentgump
                        return True
                if IsGumpCanBeClosed(currentgumpnumb):
                    CloseSimpleGump(currentgumpnumb)
        maxcounter += 1
        CheckLag(5000)
    return False

# id = 2426193729
# UOSay("a horse release")
# waitgumpid_press(id, 2)



# print(UnEquip(LegsLayer()))
# UnEquip(HatLayer())

# layers = [EarLayer(), HatLayer(), ArmsLayer(), EggsLayer(), LegsLayer(), RobeLayer(), NeckLayer(), PantsLayer()]
# for layer in layers:
#     UnEquip(layer)

print(GetGumpInfo(0))


# while Mana() >10:
#     # Wait(1500)
#     Cast('Animal Form')
#     # Wait(500)
#     # GumpButtons
# # {'X': 10, 'Y': 374, 'ReleasedID': 4017, 'PressedID': 4018, 'Quit': 1, 'PageID': 0, 'ReturnValue': 0, 'Page': 0, 'ElemNum': 7}
# # {'X': 400, 'Y': 374, 'ReleasedID': 4005, 'PressedID': 4007, 'Quit': 0, 'PageID': 2, 'ReturnValue': 0, 'Page': 1, 'ElemNum': 42}
# # {'X': 300, 'Y': 374, 'ReleasedID': 4014, 'PressedID': 4016, 'Quit': 0, 'PageID': 1, 'ReturnValue': 0, 'Page': 2, 'ElemNum': 45}
# # {'X': 400, 'Y': 374, 'ReleasedID': 4005, 'PressedID': 4007, 'Quit': 0, 'PageID': 2, 'ReturnValue': 0, 'Page': 2, 'ElemNum': 47}
# # {'X': 300, 'Y': 374, 'ReleasedID': 4014, 'PressedID': 4016, 'Quit': 0, 'PageID': 1, 'ReturnValue': 0, 'Page': 2, 'ElemNum': 50}
# # {'X': 400, 'Y': 374, 'ReleasedID': 4005, 'PressedID': 4007, 'Quit': 0, 'PageID': 2, 'ReturnValue': 0, 'Page': 2, 'ElemNum': 52}
# # {'X': 300, 'Y': 374, 'ReleasedID': 4014, 'PressedID': 4016, 'Quit': 0, 'PageID': 1, 'ReturnValue': 0, 'Page': 2, 'ElemNum': 55}
# # {'X': 400, 'Y': 374, 'ReleasedID': 4005, 'PressedID': 4007, 'Quit': 0, 'PageID': 2, 'ReturnValue': 0, 'Page': 2, 'ElemNum': 57}
# # {'X': 300, 'Y': 374, 'ReleasedID': 4014, 'PressedID': 4016, 'Quit': 0, 'PageID': 1, 'ReturnValue': 0, 'Page': 2, 'ElemNum': 60}
#     if GetGumpID(0) == 3027724650:
#         print("Its this gump")
#         # 7 frog
#         # 8 snake
#         # 3 bake kitsune
#         # 4 WOLF
#         # 5 LLama?
#         # 6 Ostard
#         # 7 yellow Ostard
#         # 8 ostard
#         # 9 ostard
#         NumGumpButton(0, 5) 
#         # Wait(1000)
#     # Wait(1000)
# SetContextMenuHook(ObjAtLayer(RhandLayer()), 0)
# while GetSkillValue('Ninjitsu') < GetSkillCap('Ninjitsu'):
#     RequestContextMenu(ObjAtLayer(RhandLayer()))
#     WaitForTarget(2000)
#     if TargetPresent():
#         TargetToObject(FindTypeEx(0x2806, 0xFFFF, Backpack(), False))
#     UseObject(ObjAtLayer(RhandLayer()))
#     WaitForTarget(2000)
#     if TargetPresent():
#         TargetToObject(FindType(0x0115, Ground()))

