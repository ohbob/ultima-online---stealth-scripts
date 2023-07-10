# ======================================================================
# Script Name: Dirty Miner
# Author: CAMOTbIK
# Version: 0.4 Beta
# EUO version tested with: 1.5 235
# Shard OSI / FS:  FS DEMISE
# Revision Date: 2023/07/07
# Public Release: 2011/11/30
# Global Variables Used: None
# Purpose: To mine.
# ======================================================================
import time
import datetime
import json
from typing import List, Any
from urllib.request import Request, urlopen
from py_stealth import *

scanRadius = 10  # how many tiles in radius to scan for resources
min_waypoint_distance = 3  # minimum distance from waypoint
travelmethod = "magery"  # "magery", "chiva", "charges", "gate"
oreBookName = "Ore"
homeBookName = "Home"
homeNumber = 1

discord_webhook = "https://discord.com/api/webhooks/88888888/9a8sdkajsdkj1k2jd918dh1kj2hdk1jhd"


tinker_menu_section = 8  # section tools
tinkermenu_tinkertools = 23  # tinker tools selection
tinkermenu_shovel = 72  # #shovel tools selection

UnloadList = [0x1BF2, 0x19BA, 0x19B9, 0x19B8, 0x19B7,  # ore
              0x3192, 0x3194, 0x3198, 0x3195, 0x3197, 0x3193]  # gems

tinkerTool = 0x1EB8
shovel = 0x0F39
storage = 0x450F0225
iron = 0x1BF2
trees = [3274, 3275, 3277, 3280, 3283, 3287, 3286, 3288, 3290, 3293, 3296, 3320, 3323, 3326, 3329, 3393, 3394, 3395,
         3396, 3415, 3416, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3476, 3478, 3480, 3482, 3484,
         3492, 3496]
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

ore_counts = {
    "start_time": time.time(),
    "Iron": {"color": 0x000, "amount": 0},
    "Shadow": {"color": 0x966, "amount": 0},
    "Copper": {"color": 0x96D, "amount": 0},
    "Bronze": {"color": 0x972, "amount": 0},
    "Gold": {"color": 0x8A5, "amount": 0},
    "Agapite": {"color": 0x979, "amount": 0},
    "Verite": {"color": 0x89F, "amount": 0},
    "Valorite": {"color": 0x8AB, "amount": 0},
}


def update_ore_counts(item):
    """
    This function updates the global ore_counts dictionary with the given item.

    Parameters:
    item (int): The item to count.
    """
    item_color = int(GetColor(item))
    item_quantity = GetQuantity(item)
    for ore in ore_counts:
        if ore != "start_time" and ore_counts[ore]["color"] == item_color:
            ore_counts[ore]["amount"] += item_quantity
            break


def calculate_ore_counts():
    """
    This function returns a string with the counts of each ore type and the ores per hour.
    """

    total = 0
    elapsed_time = time.time() - ore_counts["start_time"]
    elapsed_time_readable = str(datetime.timedelta(seconds=int(elapsed_time)))
    report = (f"-----------------------\n"
              f"Mining pace: {elapsed_time_readable}\n")
    for ore, info in ore_counts.items():
        if ore != "start_time":
            total += info["amount"]
            ores_per_hour = info["amount"] / (elapsed_time / 3600)
            report += f"{ore}: {info['amount']} / ph: {int(ores_per_hour)}\n"
    total_ores_per_hour = total / (elapsed_time / 3600)
    report += (f"Total ores per hour: {int(total_ores_per_hour)}\n"
               f"-----------------------\n")
    return report


# Helper functions


class Discord:
    def __init__(self, webhook: str, botname: str = "April O'Neil",
                 avatar: str = "https://i.pinimg.com/originals/87/67/11/876711e56a0ef942cbb2f15844235f2e.jpg"):
        self.webhook, self.botname, self.avatar = webhook, botname, avatar
        if not webhook.startswith("https://discord.com/api/webhooks/"):
            raise ValueError("Invalid webhook URL")

    def send_message(self, message: str):
        data = json.dumps({"username": self.botname, "avatar_url": self.avatar, "content": message}).encode('utf-8')
        req = Request(self.webhook, data, headers={'Content-Type': 'application/json',
                                                   'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
        urlopen(req).read()


def check(condition: bool, message: str) -> None:
    """
    Check if a condition is met and print the appropriate message.
    If the condition is not met, the script is terminated.

    Args:
        condition (bool): The condition to be checked.
        message (str): The message to be printed.

    Returns:
        None
    """
    if condition:
        print(f"PASSED => {message}")
    else:
        print(f"FAILED => {message}")
        print("TERMINATING SCRIPT, FIX THE ISSUE")
        exit()


def debug(message: str):
    current_datetime = datetime.datetime.now()
    print(current_datetime.strftime('%H:%M:%S'), message)
    ClientPrintEx(Self(), 66, 1, message)


def getxy(obj=Self()):
    return GetX(obj), GetY(obj)


def print_text_in_gumps():
    for i in range(GetGumpsCount()):
        gump = GetGumpInfo(i)

        if len(gump['XmfHTMLGumpColor']):
            for x in gump['XmfHTMLGumpColor']:
                print(GetClilocByID(x['ClilocID']).upper())

        else:
            if len(gump['Text']):
                for x in gump['Text']:
                    print(x[0].upper())


# END HELPERS

def runebook(runebookID: str, travel_method: str, rune_number: int) -> bool:
    """Travel using a runebook."""

    travel_methods = {
        'magery': list(range(-1, 100, 6)),
        'charges': list(range(-4, 98, 6)),
        'gate': list(range(0, 102, 6)),
        'chiva': list(range(1, 103, 6)),
    }

    def check_mana():
        while Mana() < 25:
            UseSkill("Meditation")
            Wait(3000)
            if Dead():
                break

    def await_xy_change(x, y, n):
        """Wait until the specified time has passed or the character's position has changed."""
        n = n / 1000  # convert milliseconds to seconds
        start_time = time.time()  # get the current time
        while True:
            current_time = time.time()  # update the current time
            elapsed_time = current_time - start_time  # calculate the elapsed time
            if elapsed_time > n or x != GetX(Self()) or y != GetY(Self()):  # if more than n seconds have passed
                return
            Wait(50)  # pause for a short time to prevent high CPU usage

    max_retries = 20
    x, y = getxy()

    debug(f"Traveling {runebookID} / {rune_number}")

    for retry in range(1, max_retries + 1):
        check_mana()

        nowx, nowy = getxy()
        if x != nowx or y != nowy:
            return True

        if Dead():
            debug("Travel EXITING -> Character is dead")
            return False

        if retry > 1:
            debug(f"Travel retry -> {retry}x")

        UseObject(runebookID)
        CheckLag(500)
        # Runebooks on Demise don't show all text, it shows only charge count, so we focus on 20 (in my case)
        if text_in_gump('20', travel_methods[travel_method][rune_number]):
            await_xy_change(GetX(Self()), GetY(Self()), 5000)

    debug(f"Travel EXITING -> Too many retries ({max_retries})")
    return False


def text_in_gump(text: str = "None", buttonid: int = None, timeout: int = 90) -> bool:
    """
    Search for text in the text/xml of a gump, if found, press buttonid

    Args:
        text (str): Text to search for
        buttonid (int): Button ID to press if the text is found
        timeout (int): Expiration time in seconds for the loop

    Returns:
        bool: True if the text is found, False otherwise
    """
    found = False
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


def find_runebooks_by_name(name: str) -> list:
    """
    Find and count the runebooks by a given name in the Backpack.

    Args:
        name (str): The name to search in runebooks.

    Returns:
        list: List of found runebook serials.
    """
    runebook_type = 0x22C5
    found_books = []

    if FindType(runebook_type, Backpack()):
        for _runebook in GetFindedList():
            tooltip = GetTooltip(_runebook)
            if name in tooltip.rsplit('|', 1)[1]:
                found_books.append(_runebook)

    return found_books


def unload():
    """
    This function unloads the mined items from the backpack to the storage.
    It also updates the global ore_counts dictionary with the unloaded items.
    """
    if NewMoveXY(GetX(storage), GetY(storage), True, 1, True):
        UseObject(storage)
        Wait(500)
        while FindTypesArrayEx(UnloadList, [0xFFFF], [Backpack()], False):
            item = FindItem()
            item_type = GetType(item)

            # If the item is an ore, update the ore counts
            if item_type in [0x1BF2, 0x19BA, 0x19B9, 0x19B8, 0x19B7]:
                update_ore_counts(item)

            MoveItem(item, 65000, storage, 0, 0, 0)
            Wait(500)
            CheckLag()


def upload():
    get_items(tinkerTool, 1, 1, storage, "Tinkertool")
    tinkering(tinkerTool, 2, tinkermenu_tinkertools, "Tinkertool")
    tinkering(shovel, 3, tinkermenu_shovel, "Shovel")
    unload()


def mine(_tile_list, _resourceBook, _runeNumber, min_waypoint_distance=0):
    """
    This function performs the mining operation.

    Parameters:
    _tile_list (list): A list of tuples, where each tuple contains the tile, x, y, and z coordinates of a mining spot.
    _resourceBook (str): The identifier for the resource book to be used for mining.
    _runeNumber (int): The number of the rune to be used for mining.
    min_waypoint_distance (int, optional): The minimum distance between waypoints. The character will only move to the next waypoint if it's further than this distance from the current waypoint. Defaults to 0.
    """

    message_fail = "You loosen some rocks| You dig some "
    message_end = ("There is nothing here |"
                   "There is no metal |"
                   "You cannot mine |"
                   "You have no line |"
                   "That is too far |"
                   "Try mining elsewhere |"
                   "You can't mine |"
                   "someone |"
                   "Target cannot be")
    message_all = message_fail + "|" + message_end + "|is attacking you"

    cave_floor_min = 1339
    cave_floor_max = 1387
    max_dig = 30

    for tile, x, y, z in _tile_list:
        if all(Dist(wp[0], wp[1], x, y) > min_waypoint_distance for wp in visited_waypoints):
            # print(f"Walking to waypoint {x, y}")
            visited_waypoints.append((x, y))

            if not NewMoveXY(x, y, True, 1, True) or Dead():
                continue

            minespot = True
            dig_count = 0

            while minespot and dig_count < max_dig:
                dig_count += 1

                if FindType(shovel, Backpack()) == 0 or Weight() > MaxWeight() - 35:
                    return False  # Indicate that unloading is needed

                UseObject(FindItem())
                WaitForTarget(5000)

                if not TargetPresent():
                    break

                start_time = datetime.datetime.now()

                if cave_floor_min <= tile <= cave_floor_max:
                    TargetToTile(tile, x, y, z)
                else:
                    print("These are mountains or rocks")
                    TargetToTile(0, x, y, z)

                if not WaitJournalLine(start_time, message_all, 2000):
                    break

                if InJournalBetweenTimes(message_end, start_time, datetime.datetime.now()) > 0:
                    minespot = False
                    Wait(500)

        # else:
        #     print("Waypoint to close")
    return True  # Indicate that mining was successful and no unloading is needed


def get_tiles(radius: int, tiles: list[int]) -> list[tuple[int, int, int, int]]:
    """
    Returns list of tiles found within the specified radius using GetLandTilesArray
    and GetStaticTilesArray functions for improved shard compatibility.

    Args:
        radius (int): Radius of search.
        tiles (list[int]): List of tile IDs to find.

    Returns:
        list[tuple[int, int, int, int]]: List of tuples representing found tiles in format (tile, x, y, z).
    """
    x, y = GetX(Self()), GetY(Self())
    min_x = x - radius
    min_y = y - radius
    max_x = x + radius
    max_y = y + radius

    found_tiles = []
    for tile in tiles:
        found_tiles.extend(GetLandTilesArray(min_x, min_y, max_x, max_y, WorldNum(), tile))
        found_tiles.extend(GetStaticTilesArray(min_x, min_y, max_x, max_y, WorldNum(), tile))

    return found_tiles


def sort_trees(trees):
    """
    Sorts trees based on their distance from the player's position.

    Args:
        trees (List[Tuple[int, int, int, int]]): List of trees represented by tuples (tile, x, y, z).

    Returns:
        List[Tuple[int, int, int, int]]: List of sorted trees.
    """

    def calculate_distance(point1, point2):
        return Dist(point1[1], point1[2], point2[1], point2[2])

    def get_key_by_distance(tree):
        return calculate_distance(tree, player_position)

    player_position = (0, GetX(Self()), GetX(Self()))
    trees_by_distance = {}

    # Group trees by rounded distance
    for tree in trees:
        distance = calculate_distance(tree, player_position)
        distance_key = distance - 1 if distance % 2 == 0 else distance
        trees_by_distance.setdefault(distance_key, []).append(tree)

    # Sort trees within groups
    ordered_trees_list = []
    for _, group in trees_by_distance.items():
        group.sort(key=get_key_by_distance)
        ordered_trees_list.extend(group)

    return ordered_trees_list


def get_items(item_type, min_amount, amount, storage, item_name=""):
    """
    Retrieves items from storage if they are below a minimum amount in the backpack.

    Args:
        item_type: The type of item to retrieve.
        min_amount: Minimum amount needed in the backpack.
        amount: Amount to retrieve from storage if below minimum amount.
        storage: The storage object ID.
        item_name (str, optional): The name of the item. Defaults to an empty string.
    """

    def wait_for_container_to_open(container_id, timeout=2000):
        """Waits for a container to open."""
        start_time = time.time()
        while (time.time() - start_time) < timeout / 1000.0:
            CheckLag()
            if LastContainer() == container_id:
                return True
            Wait(500)
        return False

    # Check if items in backpack are sufficient
    if GetQuantity(FindTypeEx(item_type, 0x0000, Backpack(), False)) >= min_amount:
        return

    # Open backpack
    UseObject(Backpack())
    Wait(500)
    CheckLag()

    # Open storage
    UseObject(storage)
    if not wait_for_container_to_open(storage):
        debug("Failed to open storage.")
        return

    # Check storage for items
    CheckLag(20000)
    if GetQuantity(FindTypeEx(item_type, 0x0000, storage, False)) >= amount:
        debug(f"Storage -> Uploading {item_name}")
        MoveItem(FindItem(), amount, Backpack(), 0, 0, 0)
        Wait(500)
    else:
        debug(f"Storage -> Out of {item_name}")
        exit()


def tinkering(item_type: int, target_amount: int, crafting_button: int, item_name: str = ""):
    """
    Craft items using a tinkering tool until a desired amount is reached in inventory.

    Args:
        item_type: The ID of the item to be crafted.
        target_amount: The desired amount of the item in inventory.
        crafting_button: The button id to be pressed in the Tinkering Menu gump.
        item_name (str, optional): The name of the item. Defaults to an empty string.
    """

    def craft_item():
        """Handle the crafting process."""
        UseType2(tinkerTool)
        text_in_gump("TINKERING MENU", tinker_menu_section, 10)
        text_in_gump("TINKERING MENU", crafting_button, 10)
        text_in_gump("TINKERING MENU", 0, 10)

    # # Check if the required amount is already in the inventory
    # current_amount = Count(item_type)
    # if current_amount >= target_amount:
    #     debug(f"Crafting -> Already have {item_name} {current_amount} / {target_amount}")
    #     return

    # Continue crafting until the desired amount is reached
    while Count(item_type) < target_amount:
        debug(f"Crafting -> {item_name} {Count(item_type)} / {target_amount}")
        get_items(iron, 10, 100, storage, "Iron")
        craft_item()

    debug(f"Crafting -> {item_name} {Count(item_type)} / {target_amount}")


def perform_diagnostic_checks():
    """
    Performs diagnostic checks before the script starts.
    Connects if not connected, and checks if character is alive,
    and required items are found.
    """
    try:
        if not Connected():
            Connect()
            Wait(2000)

        print("==============")

        check(Connected(), "CLIENT CONNECTED")
        check(not Dead(), "CHARACTER ALIVE")

        # Open backpack to get item names
        UseObject(Backpack())
        Wait(1000)

        check(len(find_runebooks_by_name(oreBookName)) > 0, "ORE BOOK NAME FOUND")
        check(len(find_runebooks_by_name(homeBookName)) > 0, "HOME BOOK NAME FOUND")
        check(Count(tinkerTool) > 0, "TOOLS TINKER FOUND")
        check(Count(shovel) > 0, "TOOLS SHOVEL FOUND")

        print("==============")
        debug("STARTING")
        print("==============")

    except Exception as e:
        print(f"An error occurred: {e}")
        exit()


# Mainloop
discord = Discord(discord_webhook)
perform_diagnostic_checks()  # Check if all prerequisites are met
oreBooks = find_runebooks_by_name(oreBookName)
homeBooks = find_runebooks_by_name(homeBookName)

while True:
    visited_waypoints = []
    for resourceBook in oreBooks:
        runeNumber = 1
        while runeNumber <= 16:  # runebook has 16 runes
            runebook(resourceBook, travelmethod, runeNumber)
            mining_successful = mine(sort_trees(get_tiles(scanRadius, caves)), resourceBook, runeNumber,
                                     min_waypoint_distance)
            if not mining_successful:
                runebook(homeBooks[0], travelmethod, homeNumber)
                unload()
                upload()
                stats = calculate_ore_counts()
                if discord_webhook.startswith("https://discord.com"):
                    discord.send_message(stats)
                else:
                    print(stats)
            else:
                runeNumber += 1  # Only move to the next rune if mining was successful
