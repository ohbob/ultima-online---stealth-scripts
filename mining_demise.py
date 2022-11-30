#======================================================================
# Script Name: Dirty Miner
# Author: CAMOTbIK
# Version: 0.3 Beta
# EUO version tested with: 1.5 235
# Shard OSI / FS:  FS DEMISE
# Revision Date: 2021/01/01
# Public Release: 2011/11/30
# Global Variables Used: None
# Purpose: To mine.
#======================================================================

from datetime import datetime
import time
from py_stealth import *

magery = list((range(-1, 100, 6)))  # 5, 11, 17, 23, 29, 35, 41, 47, 53, 59, 65, 71, 77, 83, 89, 95
charges = list((range(-4, 98, 6)))  # 2, 8, 14, 20, 26, 32, 38, 44, 50, 56, 62, 68, 74, 80, 86, 92
gate = list(range(0, 102, 6))  # 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96
chiva = list(range(1, 103, 6))  # 1, 7, 13, 19, 25, 31, 37, 43, 49, 55, 61, 67, 73, 79, 85, 91, 97

travelmethod = magery

# Runebooks
oreBookName = "Ore"
homeBookName = "Home"
homeNumber = 1

UnloadList = [0x1BF2, 0x19BA, 0x19B9, 0x19B8, 0x19B7,  # ore
              0x3192, 0x3194, 0x3198, 0x3195, 0x3197, 0x3193]  # gems

tinkerTool = 0x1EB8
shovel = 0x0F39
storage = 0x450F0225
iron = 0x1BF2

tinker_menu_section = 8  # section tools
tinkermenu_tinkertools = 23  # tinker tools selection
tinkermenu_shovel = 72  # #shovel tools selection
scanRadius = 5

caves = [1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352,
         1353, 1354, 1355, 1356, 1357, 1358, 1359, 1361, 1362, 1363, 1386
         ]  # caves

mountains = [220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 236, 237,
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
             2003, 2004, 2028, 2029, 2030, 2031, 2032, 2033, 2100, 2101, 2102, 2103, 2104, 2105
             ]  # mountains

rocks = [0x453B, 0x453C, 0x453D, 0x453E, 0x453F, 0x4540, 0x4541, 0x4542, 0x4543, 0x4544, 0x4545, 0x4546,
         0x4547, 0x4548, 0x4549, 0x454A, 0x454B, 0x454C, 0x454D, 0x454E, 0x454F
         ]  # rocks


def debug(message: str):
    now = datetime.now()
    time = f"{now.hour}:{now.minute}:{now.second} _ "
    print(f'{time}{message}')
    ClientPrintEx(Self(), 66, 1, message)


# Usage: runebook("runebook name", travel_method, rune number)
def runebook(runebook_name: str, travel_method: list[int], rune_number: int) -> bool:
    retry = 0
    x, y = GetX(Self()), GetY(Self())
    debug(f"Traveling {runebook_name} / {rune_number}")
    while GetX(Self()) == x and GetY(Self()) == y:
        if GetX(Self()) != x and GetY(Self()) != y:
            return True

        check_mana()
        retry += 1
        if retry > 1:
            debug(f"Travel retry -> {retry}x")
        if retry > 10 or Dead():
            debug(f"Travel EXITING -> Too many")
            Wait(1000)
            return False

        if find_and_use_runebook_by_name(runebook_name):
            # Runebooks on Demise don't show all text, just charges count so we focus on 20
            if text_in_gump('20', travel_method[rune_number]):
                Wait(2000)  # just to not use items too fast
    return True


def check_mana():
    while Mana() < 25:
        UseSkill("Meditation")
        Wait(5000)


def text_in_gump(text: str = "None", buttonid: int = None, timeout: int = 90) -> bool:
    """Search for text in text/xml of a gump, if found press buttonid
     Args:
        text (str): name to search for
        buttonid (int): button id to press if text found
        timeout (int): expiration of loop timeout
    Returns:
        bool: True / False
    """
    found: bool = False
    gumptimeout = time.time()
    gumpindex = None
    while not found and gumptimeout + timeout > time.time():
        for i in range(GetGumpsCount()):
            gump = GetGumpInfo(i)
            gumpindex = i
            if len(gump['XmfHTMLGumpColor']):
                for x in gump['XmfHTMLGumpColor']:
                    if text.upper() in GetClilocByID(x['ClilocID']).upper():
                        found = True
                        break
            else:
                if len(gump['Text']):
                    for x in gump['Text']:
                        if text.upper() in x[0].upper():
                            found = True
                            break
        Wait(50)

    if found and buttonid is not None:
        NumGumpButton(gumpindex, buttonid)

    return found


def find_and_use_runebook_by_name(name: str) -> bool:
    if FindType(0x22C5, Backpack()):
        for found in GetFindedList():
            if GetTooltip(found).rsplit('|', 1)[1] in name:
                UseObject(found)
                return True
        else:
            return False


def find_and_count_runebook_by_name(name: str) -> int:
    count = 0
    if FindType(0x22C5, Backpack()):
        for found in GetFindedList():
            if name in GetTooltip(found).rsplit('|', 1)[1]:
                count += 1
    return count


def unload():
    _spam = False
    if NewMoveXY(GetX(storage), GetY(storage), True, 1, True):
        UseObject(storage)
        Wait(500)
        while FindTypesArrayEx(UnloadList, [0xFFFF], [Backpack()], False):
            ClickOnObject(FindItem())
            MoveItem(FindItem(), 65000, storage, 0, 0, 0)
            Wait(500)
            # TODO
            # add spam delay check up here

            if not _spam:
                print(f"Unloading {GetAltName(FindItem())} {GetName(FindItem())}")
                _spam = True
            CheckLag()


def upload():
    get_items(tinkerTool, 1, 1, storage, "Tinkertool")
    tinkering(tinkerTool, 2, tinkermenu_tinkertools, "Tinkertool")
    tinkering(shovel, 3, tinkermenu_shovel, "Shovel")


def mine(list: list, currentrune: int, number: int):
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
                dig = 0
                while minespot:
                    if dig > 10:  # another guard if something goes south
                        break
                    else:
                        dig += 1
                    if FindType(shovel, Backpack()) > 0 and Weight() < MaxWeight() - 35:
                        UseObject(FindItem())
                        WaitForTarget(5000)
                        if TargetPresent():
                            starttime = datetime.now()
                            if tile in range(1339, 1387):
                                TargetToTile(tile, x, y, z)  # cave floor
                            else:
                                print("these are mountains or rocks")
                                TargetToTile(0, x, y, z)  # for some reason i can target only mountains.
                                # print(f'Z is {z}')

                            if WaitJournalLine(starttime, message_all, 2000):
                                # if ((InJournalBetweenTimes(message_attack, starttime, datetime.now())) > 0):
                                #     UOSay("Guards")
                                #     Wait(100)
                                if ((InJournalBetweenTimes(message_end, starttime, datetime.now())) > 0):
                                    minespot = False
                                    Wait(500)
                                    # debug(f"{tile, x, y, z}")
                                    # return True # < ------ AS WE ARE MINING ONLY ONE LAYER OF THE ROCK WE RETURN
                            else:
                                break  # did not get any messages, i guess we are trying to mine darkness
                    else:
                        runebook(homeBookName, travelmethod, homeNumber)
                        unload()
                        upload()
                        runebook(currentrune, travelmethod, number)
                        NewMoveXY(x, y, True, 1, True)
        # else:
        #     print(f"Too high Z {z}")


def get_tiles(radius: int, tiles: list[int]) -> list[tuple[int, int, int, int]]:
    """ Returns list of tiles, found in specified radius.
       Uses GetLandTilesArray + GetStaticTilesArray for improved shard compatibility.

    Args:
        radius int: Radius of search
        tiles list: List of tiles to find

    Returns
        list: List of tuples (tile, x, y, z)
    """
    x, y = GetX(Self()), GetY(Self())
    tilesxy = []
    for currenttile in tiles:
        tilesxy += GetLandTilesArray(x - radius, y - radius, x + radius, y + radius, WorldNum(), currenttile)
        tilesxy += GetStaticTilesArray(x - radius, y - radius, x + radius, y + radius, WorldNum(), currenttile)
    return tilesxy


def sort_trees(trees):
    """ @param trees List of tuples(tile,x,y,z) """
    trees_by_distance = {}
    ordered_trees_list = []
    prev_last_tree = (0, GetX(Self()), GetX(Self()))

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
                if TreeDist(tree1, tree2) > TreeDist(first_tree, last_tree):
                    first_tree, last_tree = tree1, tree2
        if TreeDist(prev_last_tree, last_tree) < TreeDist(prev_last_tree, first_tree):
            first_tree, last_tree = last_tree, first_tree
        trees.sort(key=lambda tree: TreeDist(tree, first_tree))
        ordered_trees_list += trees
        prev_last_tree = last_tree

    return ordered_trees_list


def get_items(type, minamount, amount, storage, itemstring=""):
    if GetQuantity(FindTypeEx(type, 0x0000, Backpack(), False)) < minamount:
        UseObject(Backpack())
        Wait(500)
        CheckLag()
        while LastContainer() != storage:
            UseObject(storage)
            Wait(500)
            CheckLag()
        CheckLag(20000)
        if GetQuantity(FindTypeEx(type, 0x0000, storage, False)) >= amount:
            debug(f"Storage -> Uploading {itemstring}")
            MoveItem(FindItem(), amount, Backpack(), 0, 0, 0)
            Wait(500)
        else:
            debug(f"Storage -> out of {itemstring}")
            # Wait(20000)
            exit()


def tinkering(item, amount, button, name=""):
    if amount > Count(item):
        while amount > Count(item):
            debug(f"Crafting -> {name} {Count(item)} / {amount}")
            get_items(iron, 10, 100, storage, "Iron")
            UseType2(tinkerTool)
            text_in_gump("TINKERING MENU", tinker_menu_section, 10)
            text_in_gump("TINKERING MENU", button, 10)
            text_in_gump("TINKERING MENU", 0, 10)
        debug(f"Crafting -> {name} {Count(item)} / {amount}")


def check(a, message):
    if a:
        print(f"PASSED => {message} ")
    else:
        print(f"FAILED => {message} ")
        print(f"TERMINATING SCRIPT, FIX THE ISSUE")
        exit()


def diag():
    if not Connected():
        Connect()
    print("==============")
    check(Connected(), "CLIENT CONNECTED")
    check(not Dead(), "CHARACTER ALIVE")
    UseObject(Backpack())  # Open backpack, to getitem names
    Wait(1000)
    check(find_and_count_runebook_by_name(oreBookName) > 0, "ORE BOOK NAME FOUND")
    check(find_and_count_runebook_by_name(homeBookName) > 0, "HOME BOOK NAME FOUND")
    check(Count(tinkerTool) > 0, "TOOLS TINKER FOUND")
    check(Count(shovel) > 0, "TOOLS SHOVEL FOUND")
    print("==============")
    debug("STARTING")
    print("==============")
    # if disconnected reconnect

# Mainloop
diag()  # Check if all prerequisites are met
while True:
    for bookNumber in range(0, find_and_count_runebook_by_name(oreBookName)):
        for runeNumber in range(1, 16):  # runebook has 16 runes
            currentBook = f'{oreBookName}{bookNumber}'
            runebook(currentBook, travelmethod, runeNumber)
            # mine(sort_trees(get_tiles(scanRadius, caves + mountains + rocks)), currentBook, runeNumber)
            mine(sort_trees(get_tiles(scanRadius, caves)), currentBook, runeNumber)
