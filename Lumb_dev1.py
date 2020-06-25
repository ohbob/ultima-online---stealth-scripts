from datetime import datetime
from stealth import *


def debug(message):
    print(f'{message}')
    ClientPrintEx(Self(), 66, 1, message)


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
                    waitgumpid_press(1431013363, usingregs[rune_number])
                    Wait(4000)
                else:
                    return False  # not enough reagents
            elif travel_method == "gate":
                if check_backpack([BP(), SA(), MR()]):
                    waitgumpid_press(1431013363, usinggate[rune_number])
                    Wait(4500)
                    if FindType(0x0F6C, Ground()):  # gate
                        UseObject(FindItem())
                        waitgumpid_press(3899019871, 2)
                else:
                    return False  # not enough reagents
            elif travel_method == "charge":
                runebook_gump = waitgumpid_press(1431013363, usingcharges[rune_number], False)
                if runebook_gump:
                    if 'Text' in runebook_gump:
                        if int(runebook_gump["Text"][0][0]) > 1:  # checking if we got charges
                            waitgumpid_press(1431013363, usingcharges[rune_number])
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


def check_backpack(itemlist):
    for item in itemlist:
        if not Count(item) > 0:
            debug("reg not found")
            return False  # item
    return True


def open_rb(name):
    if FindType(0x22C5, Backpack()):
        founds = GetFindedList()
        for found in founds:
            if (GetName(found)) in ('runebook: ' + name):
                UseObject(found)
                return True
    else:
        return False
    return False


# ##############################################
#
# RUNEBOOK END
#
# ##############################################


def TypeQuantity(type, color=0x0000, container=Backpack()):
    FindTypeEx(type, color, container, True)
    return FindFullQuantity()


def unload():
    storage = 0x400120D4
    NewMoveXY(751, 759, True, 0, True)
    while FindTypesArrayEx([0x1BDD], [0xFFFF], [Backpack()], False):
        MoveItem(FindItem(), 65000, storage, 0, 0, 0)
        Wait(500)


def upload():
    storage = 0x400120D4
    NewMoveXY(751, 759, True, 0, True)
    UseObject(storage)
    CheckLag(1500)
    while Count(0x0F43) < 3:
        CheckLag(5000)
        if FindTypeEx(0x0F43, 0xFFFF, storage, False) > 0:
            MoveItem(FindItem(), 1, Backpack(), 0, 0, 0)
            Wait(500)
        else:
            debug("no pickaxes found inside storage")
            Wait(60000)
    # debug("checking regs")
    # regs = (0x0F7A, 0x0F86, 0x0F7B)
    # for reg in regs:
    #     ammount = TypeQuantity(reg)
    #     if ammount <= 3:  # if found less than n regs
    #         if FindTypeEx(reg, 0x0000, storage) > 0:  # if found the reg in storage
    #             MoveItem(FindItem(), 5 - ammount, Backpack(), 0, 0, 0)
    #             Wait(500)


def mine(list):
    message_fail = "You hack at | You put some | You chop some "
    message_end = "There is nothing here |" \
                  "There's not enough |" \
                  "You cannot mine |" \
                  "You have no line |" \
                  "That is too far |" \
                  "Try mining elsewhere |" \
                  "You can't mine |" \
                  "Target cannot be"
    message_attack = "is attacking you"
    message_all = message_fail + "|" + message_end + "|" + message_attack

    for tile, x, y, z in list:
        if not Dead():
            NewMoveXY(x, y, True, 1, True)
            minespot = True
            while minespot:
                if FindType(0x0F43, Backpack()) > 0 and Weight() < MaxWeight() - 30:
                    UseObject(FindItem())
                    starttime = datetime.now()
                    WaitForTarget(5000)
                    if TargetPresent():
                        TargetToTile(tile, x, y, z)  # for some reason i can target only mountains.
                        WaitJournalLine(starttime, message_all, 120000)
                        if ((InJournalBetweenTimes(message_attack, starttime, datetime.now())) > 0):
                            UOSay("Guards")
                            Wait(100)
                        if ((InJournalBetweenTimes(message_end, starttime, datetime.now())) > 0):
                            minespot = False
                else:
                    #UnEquip(RhandLayer())
                    #Equip(RhandLayer(), 0x4019A26B)
                    #runebook("Ore", "recall", 1)  # tower
                    unload()
                    upload()
                    #runebook("Ore", "recall", 2)  # mine



def gettiles2(radius):
    temp = []
    temp2 = []
    trees = [3274, 3275, 3277, 3280, 3283, 3287, 3286, 3288, 3290, 3293, 3296, 3320, 3323, 3326, 3329, 3393, 3394, 3395, 3396, 3415, 3416, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3476, 3478, 3480, 3482, 3484, 3492, 3496]
    for currenttile in trees:
        static = GetStaticTilesArray(GetX(Self()) - radius, GetY(Self()) - radius, GetX(Self()) + radius,
                                     GetY(Self()) + radius, WorldNum(), currenttile)
        if len(static) > 0:
            temp.append(static)
    for tile in temp:
        for subtiles in tile:
            temp2.append(subtiles)
    return temp2


def SortTrees(trees):
    start_cordinates = (GetX(Self()), GetX(Self()))
    """ @param trees List of tuples(tile,x,y,z) """
    trees_by_distance = {}
    ordered_trees_list = []
    prev_last_tree = (0, start_cordinates[0], start_cordinates[1])

    def TreeDist(tree1, tree2):
        return Dist(tree1[1], tree1[2], tree2[1], tree2[2])

    for tree in trees:
        td = TreeDist(tree, prev_last_tree)
        if td % 2 == 0:
            td -= 1
        trees_group = trees_by_distance.get(td, [])
        trees_group.append(tree)
        trees_by_distance[td] = trees_group

    for current_distance in trees_by_distance:
        trees = trees_by_distance[current_distance]
        first_tree = last_tree = trees[0]
        for tree1 in trees:
            for tree2 in trees:
                if (TreeDist(tree1, tree2) > TreeDist(first_tree, last_tree)):
                    first_tree, last_tree = tree1, tree2
        if (TreeDist(prev_last_tree, last_tree) < TreeDist(prev_last_tree, first_tree)):
            first_tree, last_tree = last_tree, first_tree
        trees.sort(key=lambda tree: TreeDist(tree, first_tree))
        ordered_trees_list += trees
        prev_last_tree = last_tree
    return ordered_trees_list


if __name__ == '__main__':
    start_cordinates = (GetX(Self()), GetX(Self()))
    NewMoveXY(768, 628, True, 1, True)
    while True:
        mine(SortTrees(gettiles2(50)))
        debug("finished")
        Wait(5000)
