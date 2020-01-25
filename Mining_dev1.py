from datetime import datetime
from py_stealth import *


def debug(message):
    print(f'{message}')
    ClientPrintEx(Self(), 66, 1, message)
    ClickOnObject(FindItem)



# Usage: runebook("runebook name", "recall/gate/charges", rune number)
def runebook(runebook_name, travel_method, rune_number):
    usingregs = list((range(-1, 100, 6)))  # 5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95
    usingcharges = list((range(-4, 98, 6)))  # 2, 8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92
    usinggate = list(range(0, 102, 6))  # 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96
    check_mana()
    x, y = GetX(Self()), GetY(Self())
    while GetX(Self()) == x and GetY(Self()) == y:
        if Dead():
            return False
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
            ClickOnObject(found)
            Wait(250)
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
    storage = 0x40275C0A
    NewMoveXY(GetX(storage), GetY(storage), True, 1, True)
    while FindTypesArrayEx([0x19B9], [0xFFFF], [Backpack()], False):
        MoveItem(FindItem(), 65000, storage, 0, 0, 0)
        Wait(500)


def upload():
    storage = 0x40275C0A
    UseObject(storage)
    while Count(0x0E86) < 3:
        CheckLag(5000)
        if FindTypeEx(0x0E86, 0xFFFF, storage, False) > 0:
            MoveItem(FindItem(), 1, Backpack(), 0, 0, 0)
            Wait(500)
        else:
            debug("no pickaxes found inside storage")
            Wait(60000)
    debug("checking regs")
    regs = (0x0F7A, 0x0F86, 0x0F7B)
    for reg in regs:
        ammount = TypeQuantity(reg)
        if ammount <= 3:  # if found less than n regs
            if FindTypeEx(reg, 0x0000, storage) > 0:  # if found the reg in storage
                MoveItem(FindItem(), 5 - ammount, Backpack(), 0, 0, 0)
                Wait(500)


def mine(list):
    message_fail = "You loosen some rocks| You dig some "
    message_end = "There is nothing here |" \
                  "There is no metal |" \
                  "You cannot mine |" \
                  "You have no line |" \
                  "That is too far |" \
                  "Try mining elsewhere |" \
                  "You can't mine |" \
                  "someone |" \
                  "Target cannot be"
    message_attack = "is attacking you"
    message_all = message_fail + "|" + message_end + "|" + message_attack

    for tile, x, y, z in list:
        if not Dead():
            if NewMoveXY(x, y, True, 1, True):
                minespot = True
                while minespot:
                    if FindType(0x0E86, Backpack()) > 0 and Weight() < MaxWeight() - 30:
                        UseObject(FindItem())
                        starttime = datetime.now()
                        WaitForTarget(5000)
                        if TargetPresent():
                            if tile in range(1339, 1387):
                                TargetToTile(tile, x, y, z)  # cave floor
                            else:
                                TargetToTile(0, x, y, z)  # for some reason i can target only mountains.
                                print(f'Z is {z}')
                            UseType2(0x0E9D)
                            WaitJournalLine(starttime, message_all, 120000)
                            # if ((InJournalBetweenTimes(message_attack, starttime, datetime.now())) > 0):
                            #     UOSay("Guards")
                            #     Wait(100)
                            if ((InJournalBetweenTimes(message_end, starttime, datetime.now())) > 0):
                                minespot = False
                    else:
                        runebook("Ore", "recall", 1)  # tower
                        unload()
                        upload()
                        runebook("Ore", "recall", 4)  # mine
        # else:
        #     print(f"Too high Z {z}")


def gettiles2(radius):
    temp = []
    temp2 = []
    caves = (1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352,
                1353, 1354, 1355, 1356, 1357, 1358, 1359, 1361, 1362, 1363, 1386) # caves 
    mountains = (220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 236, 237,
                238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261,
                262, 263, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 286, 287, 288, 289, 290, 291,
                292, 293, 294, 296, 296, 297, 321, 322, 323, 324, 467, 468, 469, 470, 471, 472, 473, 474, 476, 477,
                478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 492, 493, 494, 495, 543, 544, 545, 546, 547, 548,
                549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568,
                569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 581, 582, 583, 584, 585, 586, 587, 588, 589,
                590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 610, 611, 612, 613, 1010, 1741, 1742,
                1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1771,
                1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1781, 1782, 1783, 1784, 1785, 1786, 1787,
                1788, 1789, 1790, 1801, 1802, 1803, 1804, 1805, 1806, 1807, 1808, 1809, 1811, 1812, 1813, 1814,
                1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1831, 1832, 1833, 1834, 1835, 1836,
                1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852,
                1853, 1854, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874,
                1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1981, 1982, 1983, 1984, 1985, 1986,
                1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
                2003, 2004, 2028, 2029, 2030, 2031, 2032, 2033, 2100, 2101, 2102, 2103, 2104, 2105) # mountains 
    rocks = (0x453B, 0x453C, 0x453D, 0x453E, 0x453F, 0x4540, 0x4541, 0x4542, 0x4543, 0x4544, 0x4545, 0x4546, 
                0x4547, 0x4548, 0x4549, 0x454A, 0x454B, 0x454C, 0x454D, 0x454E, 0x454F) # rocks

    for currenttile in caves, mountains, rocks:
        land = GetLandTilesArray(GetX(Self()) - radius, GetY(Self()) - radius, GetX(Self()) + radius,
                                 GetY(Self()) + radius, WorldNum(), currenttile)
        if len(land) > 0:
            temp.append(land)
        static = GetStaticTilesArray(GetX(Self()) - radius, GetY(Self()) - radius, GetX(Self()) + radius,
                                     GetY(Self()) + radius, WorldNum(), currenttile)
        if len(static) > 0:
            temp.append(static)

    for tile in temp:
        for subtiles in tile:
            temp2.append(subtiles)
    return temp2


def SortTrees(trees):
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
    while True:
        mine(SortTrees(gettiles2(40)))

