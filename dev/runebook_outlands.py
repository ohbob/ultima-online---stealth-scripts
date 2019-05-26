from stealth_py import *


# Usage: runebook("runebook name", "recall/gate/charges", rune number)
def runebook(runebook_name, travel_method, rune_number):
    usingregs = list((range(-1, 100, 6)))  # 5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95
    usingcharges = list((range(-4, 98, 6)))  # 2, 8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92
    usinggate = list(range(0, 102, 6))  # 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96

    check_mana()

    x, y = GetX(Self()), GetY(Self())
    while GetX(Self()) == x and GetY(Self()) == y:
        if open_rb(runebook_name):
            if travel_method == "recall":
                if check_backpack([BP(), BM(), MR()]):
                    waitgumpid_press(1551740969, usingregs[rune_number])
                    Wait(4000)
                else:
                    return False  # not enough reagents

            elif travel_method == "gate":
                if check_backpack([BP(), SA(), MR()]):
                    waitgumpid_press(1551740969, usinggate[rune_number])
                    Wait(4500)
                    if FindType(0x0F6C, Ground()):  # gate
                        UseObject(FindItem())
                        waitgumpid_press(3899019871, 2)
                else:
                    return False  # not enough reagents

            elif travel_method == "charge":
                runebook_gump = waitgumpid_press(1551740969, usingcharges[rune_number], False)
                if runebook_gump:
                    if 'Text' in runebook_gump:
                        if int(runebook_gump["Text"][0][0]) > 1:  # checking if we got charges
                            waitgumpid_press(1551740969, usingcharges[rune_number])
                            Wait(4000)
                        else:
                            return False  # less than minimum charges

            else:
                return False  # invalid travel method
        Wait(500)
    return True


def check_mana():
    while Mana() < 25:
        UseSkill("Meditation")
        Wait(5000)


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
        CheckLag(100000)
    return False


GetExtInfo()

def check_backpack(itemlist):
    for item in itemlist:
        if not Count(item) > 0:
            return False  # item
    return True


def open_rb(name):
    if FindType(0x22C5, Backpack()):
        founds = GetFindedList()
        for found in founds:
            if (GetName(found)) in ('runebook: ' + name):
                UseObject(found)
                return True  # found the named runebook
    else:
        return False  # didn't find anything


if __name__ == '__main__':
    runebook("Towns", "recall", 3)
    runebook("Towns", "gate", 2)
    runebook("Towns", "charge", 1)
