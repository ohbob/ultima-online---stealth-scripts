# ======================================================================
# Universal Resource Gathering Bot - Professional Edition
# ======================================================================
# Author: CAMOTbIK
# Version: 0.1 BETA
# Last Updated: 2025
# 
# Purpose: 
#   - Universal resource gathering (mining, lumberjacking, fishing)
#   - TSP route optimization with intelligent caching
#   - Performance monitoring and bottleneck detection
#   - Automatic tool crafting and inventory management
#   - Discord integration for remote monitoring
#
# Features:
#   - Class-based architecture for maintainability
#   - Configurable resource types and crafting recipes
#   - Real-time performance timing with debug mode
#   - Universal resource tracking and reporting
#   - Progressive enhancement with error handling
#
# Usage:
#   1. Configure resource types and settings
#   2. Set DEBUG_MODE for performance monitoring
#   3. Run script and monitor via Discord
# ======================================================================
import time
import datetime
import json
import os
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from py_stealth import *


# ===== CONFIGURATION =====
# ===== SET YOUR RESOURCE TYPE HERE =====
# Choose one: "mining", "lumberjacking", or "fishing"
RESOURCE_TYPE = "mining"  # Change this to switch activities

# Resource-specific scan radii (trees are more spread out than ore)
MINING_SCAN_RADIUS = 10
LUMBERJACKING_SCAN_RADIUS = 200
FISHING_SCAN_RADIUS = 200

# Resource-specific waypoint distances (mining needs spacing, lumberjacking less so)
MINING_WAYPOINT_DISTANCE = 3      # Avoid revisiting same mining spots
LUMBERJACKING_WAYPOINT_DISTANCE = 0  # Trees are naturally spaced, no need for restriction
FISHING_WAYPOINT_DISTANCE = 0     # Some spacing for fishing spots

TRAVEL_METHOD = "magery"  # "magery", "chiva", "charges", "gate"

# Resource book names
ORE_BOOK_NAME = "Ore"
LUMBER_BOOK_NAME = "Lumber"
FISHING_BOOK_NAME = "Fishing"
HOME_BOOK_NAME = "Home"
HOME_NUMBER = 1
DISCORD_WEBHOOK = ""
DISCORD_MESSAGE_INTERVAL = 60  # Send Discord message every X minutes (0 = every run)
DEBUG_MODE = False  # Enable performance timing and debug output



# ===== ITEM IDS =====
# Tools and crafting items
TINKER_TOOL = 0x1EB8      # Tinkering tool for crafting
SHOVEL = 0x0F39           # Mining shovel
HATCHET = 0x0F43          # Lumberjacking hatchet
FISHING_POLE = 0x0DC0     # Fishing pole
BOARD = 0x1BD7            # Boards for crafting
IRON = 0x1BF2             # Iron ingots for crafting
STORAGE = 0x450F0225      # Storage container ID


# Items to unload to storage (ores and gems)
UNLOAD_LIST = [
    # Ores
    0x1BF2,  # Iron
    0x19BA,  # Shadow
    0x19B9,  # Copper  
    0x19B8,  # Bronze
    0x19B7,  # Gold
    # Gems
    0x3192,  # Diamond
    0x3194,  # Emerald
    0x3198,  # Ruby
    0x3195,  # Sapphire
    0x3197,  # Amethyst
    0x3193   # Topaz
]

# ===== TILE TYPES =====
CAVES = [1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352,
         1353, 1354, 1355, 1356, 1357, 1358, 1359, 1361, 1362, 1363, 1386]

MOUNTAINS = [220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 236, 237,
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
             2003, 2004, 2028, 2029, 2030, 2031, 2032, 2033, 2100, 2101, 2102, 2103, 2104, 2105]

ROCKS = [0x453B, 0x453C, 0x453D, 0x453E, 0x453F, 0x4540, 0x4541, 0x4542, 0x4543, 0x4544, 0x4545, 0x4546,
         0x4547, 0x4548, 0x4549, 0x454A, 0x454B, 0x454C, 0x454D, 0x454E, 0x454F]

TREES = [3274, 3275, 3277, 3280, 3283, 3287, 3286, 3288, 3290, 3293, 3296, 3320, 3323, 3326, 3329, 3393, 3394, 3395,
         3396, 3415, 3416, 3418, 3419, 3438, 3439, 3440, 3441, 3442, 3460, 3461, 3462, 3476, 3478, 3480, 3482, 3484,
         3492, 3496]
CAVES = [1339, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1351, 1352,
         1353, 1354, 1355, 1356, 1357, 1358, 1359, 1361, 1362, 1363, 1386
         ]  # caves

WATER_TILES = []         



class Utils:
    """Universal game utility functions for UO automation"""
    
    @staticmethod
    def debug(message):
        current_datetime = datetime.datetime.now()
        print(current_datetime.strftime('%H:%M:%S'), message)
        ClientPrintEx(Self(), 66, 1, message)
    
    @staticmethod
    def check(condition, message):
        """Check condition and exit if failed"""
        if condition:
            print(f"✅ PASSED => {message}")
        else:
            print(f"❌ FAILED => {message}")
            print("🛑 TERMINATING SCRIPT, FIX THE ISSUE")
            exit()
    
    @staticmethod
    def log_error(error, context=""):
        """Log errors with context for debugging"""
        error_msg = f"🚨 ERROR in {context}: {str(error)}"
        Utils.debug(error_msg)
        if DEBUG_MODE:
            import traceback
            Utils.debug(f"📋 Stack trace: {traceback.format_exc()}")
    
    @staticmethod
    def log_warning(message):
        """Log warnings for non-critical issues"""
        Utils.debug(f"⚠️ WARNING: {message}")
    
    @staticmethod
    def log_success(message):
        """Log successful operations"""
        Utils.debug(f"✅ SUCCESS: {message}")
    
    @staticmethod
    def format_label(key: str) -> str:
        """Cheap label formatter: turn snake_case or camelCase into Title Case."""
        try:
            # Replace underscores, split camelCase, and title-case
            import re
            spaced = re.sub(r"(_)+", " ", key)
            spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", spaced)
            return spaced.strip().title()
        except Exception:
            return key
    
    @staticmethod
    def getxy(obj=Self()):
        return GetX(obj), GetY(obj)
    
    @staticmethod
    def text_in_gump(text="None", buttonid=None, timeout=90):
        """Search for text in gump and press button if found"""
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
                
                if found:
                    break
            
            if not found:
                Wait(50)
        
        if found and buttonid is not None:
            Wait(500)
            NumGumpButton(gumpindex, buttonid)
            Wait(500)
        
        return found
    
    @staticmethod
    def timer(func):
        """
        Decorator to measure and print the execution time of a function.
        
        Usage:
            @Utils.timer
            def my_function():
                # your code here
                pass
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not DEBUG_MODE:
                return func(*args, **kwargs)
            
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            Utils.debug(f"⏱️ {func.__name__} executed in {execution_time:.4f} seconds")
            return result
        return wrapper
    



class TileScanner:
    """Handles tile scanning and detection"""
    
    def __init__(self):
        self.caves = CAVES
        self.mountains = MOUNTAINS
        self.rocks = ROCKS
    
    @Utils.timer
    def get_tiles(self, radius: int, tiles):
        """Parallel processing version using ThreadPoolExecutor"""
        world = WorldNum()
        x, y = GetX(Self()), GetY(Self())
        min_x = x - radius
        min_y = y - radius
        max_x = x + radius
        max_y = y + radius

        def get_tile_data(tile):
            land_tiles = GetLandTilesArray(min_x, min_y, max_x, max_y, world, tile)
            static_tiles = GetStaticTilesArray(min_x, min_y, max_x, max_y, world, tile)
            return land_tiles + static_tiles

        found_tiles = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(get_tile_data, tile) for tile in tiles]
            for future in futures:
                found_tiles.extend(future.result())
        
        return found_tiles


class CoordinateManager:
    """Unified coordinate management for caching and blacklisting"""
    
    def __init__(self):
        self.tsp_cache = {}
        self.blacklisted_coords = {}
        self.load_all_data()
    
    def load_all_data(self):
        """Load both TSP cache and blacklist data"""
        # Load TSP cache
        try:
            with open("tsp_cache.json", "r") as f:
                self.tsp_cache = json.load(f)
        except:
            self.tsp_cache = {}
        
        # Load blacklist
        try:
            with open("resource_blacklist.json", "r") as f:
                self.blacklisted_coords = json.load(f)
        except:
            self.blacklisted_coords = {}
    
    def save_all_data(self):
        """Save both TSP cache and blacklist data"""
        # Save TSP cache
        with open("tsp_cache.json", "w") as f:
            json.dump(self.tsp_cache, f)
        
        # Save blacklist
        with open("resource_blacklist.json", "w") as f:
            json.dump(self.blacklisted_coords, f, indent=2)
    
    def get_coord_key(self, x, y):
        """Generate consistent coordinate key"""
        return f"{x}_{y}"
    
    def is_blacklisted(self, x, y):
        """Check if coordinates are blacklisted"""
        return self.get_coord_key(x, y) in self.blacklisted_coords
    
    def add_to_blacklist(self, x, y, reason="can't be seen"):
        """Add coordinates to blacklist"""
        coord_key = self.get_coord_key(x, y)
        if coord_key not in self.blacklisted_coords:
            self.blacklisted_coords[coord_key] = {
                "x": x,
                "y": y,
                "reason": reason,
                "added_time": time.time()
            }
            Utils.debug(f"🚫 Added to blacklist: {x},{y} - {reason}")
            self.save_all_data()
    
    def get_blacklist_stats(self):
        """Get blacklist statistics"""
        return {
            "total_blacklisted": len(self.blacklisted_coords),
            "blacklisted_coords": self.blacklisted_coords
        }
    
    def get_cache_stats(self):
        """Get cache hit/miss statistics"""
        return {
            'cache_hits': getattr(self, 'cache_hits', 0),
            'cache_misses': getattr(self, 'cache_misses', 0)
        }
    
    def reset_cache_stats(self):
        """Reset cache statistics"""
        self.cache_hits = 0
        self.cache_misses = 0


class TSPOptimizer:
    """Handles TSP route optimization and caching"""
    
    def __init__(self, coord_manager):
        self.coord_manager = coord_manager
    
    @Utils.timer
    def adapted_tsp_algorithm(self, dataset, tsp_algorithm):
        # Create a mapping from (x, y) to the full data tuple
        xy_to_full_data = {(x, y): full_data for full_data in dataset for _, x, y, _ in [full_data]}
        
        # Extract x and y coordinates from dataset
        points = [(x, y) for _, x, y, _ in dataset]
        
        # Calculate the route using the given TSP algorithm
        path, length = self.calculate_route(points, tsp_algorithm)
        
        # Map the sorted (x, y) path back to the original dataset format
        adapted_path = [xy_to_full_data[(x, y)] for x, y in path]
        
        return adapted_path, int(length), 0  # Timer decorator handles timing
    
    def two_opt_tsp(self, points, dist_matrix):
        def two_opt_swap(route, i, k):
            return route[:i] + route[i:k + 1][::-1] + route[k + 1:]

        num_points = len(points)
        best_route = list(range(num_points))
        improved = True

        while improved:
            improved = False
            best_distance = sum(dist_matrix[best_route[i - 1]][best_route[i]] for i in range(1, num_points))
            for i in range(1, num_points - 1):
                for k in range(i + 1, num_points):
                    new_route = two_opt_swap(best_route, i, k)
                    new_distance = sum(dist_matrix[new_route[j - 1]][new_route[j]] for j in range(1, num_points))
                    if new_distance < best_distance:
                        best_route = new_route
                        best_distance = new_distance
                        improved = True

        return [points[i] for i in best_route], best_distance
    
    def calculate_route(self, points, tsp_algorithm):
        def calculate_distance(point1, point2):
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

        def calculate_all_distances():
            num_points = len(points)
            dist_matrix = [[0] * num_points for _ in range(num_points)]
            for i in range(num_points):
                for j in range(i + 1, num_points):
                    dist = calculate_distance(points[i], points[j])
                    dist_matrix[i][j] = dist_matrix[j][i] = dist
            return dist_matrix

        dist_matrix = calculate_all_distances()
        return tsp_algorithm(points, dist_matrix)
    
    @Utils.timer
    def cached_adapted_tsp_algorithm(self, dataset, tsp_algorithm):
        x, y = GetX(Self()), GetY(Self())
        key = self.coord_manager.get_coord_key(x, y)
        
        if key in self.coord_manager.tsp_cache:
            if DEBUG_MODE:
                Utils.debug(f"📋 TSP Cache HIT -> Using cached route for {key}")
            self.cache_hits = getattr(self, 'cache_hits', 0) + 1
            return self.coord_manager.tsp_cache[key]
        
        if DEBUG_MODE:
            Utils.debug(f"🔄 TSP Cache MISS -> Computing new route for {key}")
        self.cache_misses = getattr(self, 'cache_misses', 0) + 1
        result = self.adapted_tsp_algorithm(dataset, tsp_algorithm)
        self.coord_manager.tsp_cache[key] = result
        self.coord_manager.save_all_data()
        return result

    def get_cache_stats(self):
        """Expose hit/miss stats for final reporting."""
        return {
            'cache_hits': getattr(self, 'cache_hits', 0),
            'cache_misses': getattr(self, 'cache_misses', 0)
        }

    def reset_cache_stats(self):
        self.cache_hits = 0
        self.cache_misses = 0


class TravelManager:
    """Handles travel and runebook operations"""
    
    def __init__(self):
        self.travel_methods = {
            'magery': list(range(-1, 100, 6)),
            'charges': list(range(-4, 98, 6)),
            'gate': list(range(0, 102, 6)),
            'chiva': list(range(1, 103, 6)),
        }
    
    @Utils.timer
    def runebook(self, runebookID: str, travel_method: str, rune_number: int, book_name: str = "Unknown", book_index: int = 1) -> bool:
        """Travel using a runebook"""
        def check_mana():
            while Mana() < 25:
                UseSkill("Meditation")
                Wait(3000)
                if Dead():
                    break

        def await_xy_change(x, y, n):
            n = n / 1000
            start_time = time.time()
            while True:
                current_time = time.time()
                elapsed_time = current_time - start_time
                
                if x != GetX(Self()) or y != GetY(Self()):
                    Utils.debug("Position changed")
                    return
                    
                if elapsed_time > n:
                    return
                    
                Wait(50)

        max_retries = 20
        x, y = Utils.getxy()

        # Show descriptive book name with book index and rune number
        if book_name != "Unknown":
            book_display = f"{book_name} {book_index}/{rune_number}"
        else:
            book_display = f"Book_{book_index}/{rune_number}"
        Utils.debug(f"Runebook -> {book_display}")

        for retry in range(1, max_retries + 1):
            check_mana()

            nowx, nowy = Utils.getxy()
            if x != nowx or y != nowy:
                return True

            if Dead():
                Utils.debug("💀 Travel EXITING -> Character is dead")
                return False

            if retry > 1:
                Utils.debug(f"🔄 Travel retry -> {retry}x")

            UseObject(runebookID)
            CheckLag(500)
            if Utils.text_in_gump('20', self.travel_methods[travel_method][rune_number]):
                await_xy_change(GetX(Self()), GetY(Self()), 5000)

        Utils.debug(f"❌ Travel EXITING -> Too many retries ({max_retries})")
        return False
    
    def find_runebooks_by_name(self, name: str) -> list:
        """Find runebooks by name in backpack"""
        runebook_type = 0x22C5
        found_books = []

        if FindType(runebook_type, Backpack()):
            for _runebook in GetFindedList():
                tooltip = GetTooltip(_runebook)
                if name in tooltip.rsplit('|', 1)[1]:
                    found_books.append(_runebook)

        return found_books


class InventoryManager:
    """Handles inventory, storage, and crafting operations"""
    
    def __init__(self):
        self.tinker_menu_section = 8
        self.tinkermenu_tinkertools = 23
        self.tinkermenu_shovel = 72
    
    @Utils.timer
    def get_items(self, item_type, min_amount, amount, storage, item_name=""):
        """Retrieve items from storage if below minimum"""
        def wait_for_container_to_open(container_id, timeout=2000):
            start_time = time.time()
            while (time.time() - start_time) < timeout / 1000.0:
                CheckLag()
                if LastContainer() == container_id:
                    return True
                Wait(500)
            return False

        if GetQuantity(FindTypeEx(item_type, 0x0000, Backpack(), False)) >= min_amount:
            return

        UseObject(Backpack())
        Wait(500)
        CheckLag()

        UseObject(storage)
        if not wait_for_container_to_open(storage):
            Utils.debug("Failed to open storage.")
            return

        CheckLag(20000)
        if GetQuantity(FindTypeEx(item_type, 0x0000, storage, False)) >= amount:
            Utils.debug(f"Storage -> Uploading {item_name}")
            MoveItem(FindItem(), amount, Backpack(), 0, 0, 0)
            Wait(500)
        else:
            Utils.debug(f"Storage -> Out of {item_name}")
            exit()
    
    @Utils.timer
    def unload(self, resource_tracker):
        """Unload items to storage and update resource counts"""
        if NewMoveXY(GetX(STORAGE), GetY(STORAGE), True, 1, True):
            UseObject(STORAGE)
            Wait(500)
            while FindTypesArrayEx(UNLOAD_LIST, [0xFFFF], [Backpack()], False):
                item = FindItem()
                # item_type = GetType(item)

                # Update tracker with the item (it will handle different resource types)
                resource_tracker.update_counts(item)

                MoveItem(item, 65000, STORAGE, 0, 0, 0)
                Wait(500)
                CheckLag()
    
    def upload(self, resource_tracker, stats=None):
        """Upload tools and craft if needed"""
        self.get_items(TINKER_TOOL, 1, 1, STORAGE, "Tinkertool")
        self.tinkering(TINKER_TOOL, 2, self.tinkermenu_tinkertools, "Tinkertool", stats)
        self.tinkering(SHOVEL, 3, self.tinkermenu_shovel, "Shovel", stats)
    
    def tinkering(self, item_type: int, target_amount: int, crafting_button: int, item_name: str = "", stats=None):
        """Craft items using tinkering"""
        def craft_item():
            UseType2(TINKER_TOOL)
            Utils.text_in_gump("TINKERING MENU", self.tinker_menu_section, 10)
            Utils.text_in_gump("TINKERING MENU", crafting_button, 10)
            Utils.text_in_gump("TINKERING MENU", 0, 10)

        initial_count = Count(item_type)
        while Count(item_type) < target_amount:
            Utils.debug(f"Crafting -> {item_name} {Count(item_type)} / {target_amount}")
            self.get_items(IRON, 10, 100, STORAGE, "Iron")
            craft_item()
            
            # Track materials used (10 iron per tool)
            if stats and Count(item_type) > initial_count:
                stats['materials_used']['iron_ingots'] += 10
                if item_name.lower() == "shovel":
                    stats['tools_crafted']['shovels'] += 1
                elif item_name.lower() == "hatchet":
                    stats['tools_crafted']['hatchets'] += 1
                elif item_name.lower() == "fishing pole":
                    stats['tools_crafted']['fishing_poles'] += 1
                    stats['materials_used']['boards'] += 1  # Fishing poles need boards
                elif item_name.lower() == "tinkertool":
                    stats['tools_crafted']['tinkering_tools'] += 1
                initial_count = Count(item_type)

        Utils.debug(f"Crafting -> {item_name} {Count(item_type)} / {target_amount}")


class ResourceGatherer:
    """Universal resource gathering operations (mining, lumberjacking, fishing, etc.)"""
    
    def __init__(self, coord_manager):
        self.visited_waypoints = []
        self.coord_manager = coord_manager
        
        # Resource type configurations
        self.resource_configs = {
            'mining': {
                'tool_type': SHOVEL,
                'tool_name': 'Shovel',
                'max_attempts': 30,
                'tiles': [CAVES, MOUNTAINS, ROCKS],  # Multiple tile types for mining
                'crafting': {
                    'tool_id': SHOVEL,
                    'crafting_button': 72,  # Shovel button in tinkering menu
                    'materials': {IRON: 10},  # 10 iron needed per shovel
                    'target_amount': 3  # Keep 3 shovels in inventory
                },
                'messages': {
                    'fail': "You loosen some rocks| You dig some ",
                    'end': ("There is nothing here |"
                           "There is no metal |"
                           "You cannot mine |"
                           "You have no line |"
                           "That is too far |"
                           "Try mining elsewhere |"
                           "You can't mine |"
                           "someone |"
                           "Target cannot be"),
                    'all': None
                },
                'tile_ranges': [(1339, 1387)],  # Cave floor range
                'weight_limit': 35
            },
            'lumberjacking': {
                'tool_type': HATCHET,
                'tool_name': 'Hatchet',
                'max_attempts': 20,
                'tiles': [TREES],  # Tree tile types
                'crafting': {
                    'tool_id': HATCHET,
                    'crafting_button': 73,  # Hatchet button in tinkering menu
                    'materials': {IRON: 8},  # 8 iron needed per hatchet
                    'target_amount': 3
                },
                'messages': {
                    'fail': "You chop some wood| You cut some ",
                    'end': ("There is nothing here |"
                           "You cannot cut |"
                           "That is too far |"
                           "Try cutting elsewhere |"
                           "You can't cut |"
                           "someone |"
                           "Target cannot be"),
                    'all': None
                },
                'tile_ranges': [],
                'weight_limit': 35
            },
            'fishing': {
                'tool_type': FISHING_POLE,
                'tool_name': 'Fishing Pole',
                'max_attempts': 15,
                'tiles': [WATER_TILES],  # Water tile types
                'crafting': {
                    'tool_id': FISHING_POLE,
                    'crafting_button': 74,  # Fishing pole button in tinkering menu
                    'materials': {IRON: 5, BOARD: 1},  # 5 iron + 1 board per pole
                    'target_amount': 2
                },
                'messages': {
                    'fail': "You pull out a fish| You catch some ",
                    'end': ("There is nothing here |"
                           "You cannot fish |"
                           "That is too far |"
                           "Try fishing elsewhere |"
                           "You can't fish |"
                           "someone |"
                           "Target cannot be"),
                    'all': None
                },
                'tile_ranges': [],
                'weight_limit': 35
            }
        }
        
        # Build message_all for each resource type
        for resource_type, config in self.resource_configs.items():
            config['messages']['all'] = (config['messages']['fail'] + "|" + 
                                       config['messages']['end'] + "|is attacking you")
    
    def add_to_blacklist(self, x, y, reason="can't be seen"):
        """Add coordinates to blacklist"""
        self.coord_manager.add_to_blacklist(x, y, reason)
    
    def is_blacklisted(self, x, y):
        """Check if coordinates are blacklisted"""
        return self.coord_manager.is_blacklisted(x, y)
    
    def get_blacklist_stats(self):
        """Get blacklist statistics"""
        return self.coord_manager.get_blacklist_stats()
    
    @Utils.timer
    def gather(self, resource_type, tile_list, resource_book, rune_number, min_waypoint_distance=0, stats=None):
        """Universal resource gathering operation"""
        if resource_type not in self.resource_configs:
            Utils.debug(f"❌ Unknown resource type: {resource_type}")
            return False
            
        config = self.resource_configs[resource_type]
        tool_type = config['tool_type']
        tool_name = config['tool_name']
        max_attempts = config['max_attempts']
        messages = config['messages']
        tile_ranges = config['tile_ranges']
        weight_limit = config['weight_limit']

        for tile, x, y, z in tile_list:
            # Check if coordinates are blacklisted
            if self.is_blacklisted(x, y):
                Utils.debug(f"🚫 Skipping blacklisted coordinates: {x},{y}")
                continue
                
            if all(Dist(wp[0], wp[1], x, y) > min_waypoint_distance for wp in self.visited_waypoints):
                self.visited_waypoints.append((x, y))

                if not NewMoveXY(x, y, True, 1, True) or Dead():
                    continue

                gathering = True
                attempt_count = 0

                while gathering and attempt_count < max_attempts:
                    attempt_count += 1
                    
                    # Increment gathering attempts counter for each tool swing
                    if stats:
                        stats['total_gathering_attempts'] += 1

                    if FindType(tool_type, Backpack()) == 0 or Weight() > MaxWeight() - weight_limit:
                        return False

                    UseObject(FindItem())
                    WaitForTarget(5000)

                    if not TargetPresent():
                        break

                    start_time = datetime.datetime.now()

                    # Handle different targeting based on resource type
                    if resource_type == 'mining' and tile_ranges:
                        # Check if tile is in any of the configured ranges
                        use_special_targeting = any(
                            tile_range[0] <= tile <= tile_range[1] 
                            for tile_range in tile_ranges
                        )
                        if use_special_targeting:
                            TargetToTile(tile, x, y, z)
                        else:
                            TargetToTile(0, x, y, z)
                    else:
                        # For lumberjacking, fishing, etc. - target the tile directly
                        TargetToTile(tile, x, y, z)

                    if not WaitJournalLine(start_time, messages['all'], 2000):
                        break

                    # Check for "can't be seen" messages and blacklist coordinates
                    if InJournalBetweenTimes("can't be seen", start_time, datetime.datetime.now()) > 0:
                        self.add_to_blacklist(x, y, "can't be seen")
                        gathering = False
                        Wait(500)
                        break

                    if InJournalBetweenTimes(messages['end'], start_time, datetime.datetime.now()) > 0:
                        gathering = False
                        Wait(500)

        return True
    
    def add_resource_type(self, resource_type, tool_type, tool_name, max_attempts, 
                         fail_messages, end_messages, tiles=None, tile_ranges=None, 
                         weight_limit=35, crafting_config=None):
        """Add a new resource type configuration"""
        self.resource_configs[resource_type] = {
            'tool_type': tool_type,
            'tool_name': tool_name,
            'max_attempts': max_attempts,
            'tiles': tiles or [],
            'crafting': crafting_config,
            'messages': {
                'fail': fail_messages,
                'end': end_messages,
                'all': fail_messages + "|" + end_messages + "|is attacking you"
            },
            'tile_ranges': tile_ranges or [],
            'weight_limit': weight_limit
        }
    
    def get_tiles_for_resource(self, resource_type):
        """Get all tile arrays for a specific resource type"""
        if resource_type not in self.resource_configs:
            return []
        
        # Flatten the tiles array (combine all tile types for this resource)
        all_tiles = []
        for tile_array in self.resource_configs[resource_type]['tiles']:
            all_tiles.extend(tile_array)
        
        return all_tiles


class ResourceTracker:
    """Universal resource tracker for ores, lumber, fish, etc."""
    
    def __init__(self, resource_type="mining"):
        self.resource_type = resource_type
        self.start_time = time.time()
        
        # Predefined resource configurations
        self.resource_configs = {
            "mining": {
                "title": "Mining",
                "items": {
                    "Iron": {"type": [0x19B7, 0x19B8, 0x19B9], "color": 0x000, "amount": 0},
                    "Shadow": {"type": [0x19B7, 0x19B8, 0x19B9], "color": 0x966, "amount": 0},
                    "Copper": {"type": [0x19B7, 0x19B8, 0x19B9], "color": 0x96D, "amount": 0},
                    "Bronze": {"type": [0x19B7, 0x19B8, 0x19B9], "color": 0x972, "amount": 0},
                    "Gold": {"type": [0x19B7, 0x19B8, 0x19B9], "color": 0x8A5, "amount": 0},
                    "Agapite": {"type": [0x19B7, 0x19B8, 0x19B9], "color": 0x979, "amount": 0},
                    "Verite": {"type": [0x19B8, 0x19B9, 0x19BA], "color": 0x89F, "amount": 0},
                    "Valorite": {"type": [0x19B9, 0x19BA, 0x19BB], "color": 0x8AB, "amount": 0},
                    "Amethyst": {"type": 0x3195, "amount": 0},
                    "Citrine": {"type": 0x3194, "amount": 0},
                    "Diamond": {"type": 0x3198, "amount": 0},
                    "Emerald": {"type": 0x3193, "amount": 0},
                    "Ruby": {"type": 0x3197, "amount": 0},
                    "Sapphire": {"type": 0x3192, "amount": 0},
                    "Star Sapphire": {"type": 0x5732, "amount": 0},
                    "Tourmaline": {"type": 0x0F28, "amount": 0},
                }
            },
            "lumberjacking": {
                "title": "Lumberjacking",
                "items": {
                    "Regular Wood": {"type": [0x1BD7, 0x1BD8, 0x1BD9], "color": 0x000, "amount": 0},
                    "Oak Wood": {"type": [0x1BD7, 0x1BD8, 0x1BD9], "color": 0x7DA, "amount": 0},
                    "Ash Wood": {"type": [0x1BD7, 0x1BD8, 0x1BD9], "color": 0x7A1, "amount": 0},
                    "Yew Wood": {"type": [0x1BD7, 0x1BD8, 0x1BD9], "color": 0x7A8, "amount": 0},
                    "Heartwood": {"type": [0x1BD7, 0x1BD8, 0x1BD9], "color": 0x7A9, "amount": 0},
                    "Bloodwood": {"type": [0x1BD7, 0x1BD8, 0x1BD9], "color": 0x7AA, "amount": 0},
                    "Frostwood": {"type": [0x1BD7, 0x1BD8, 0x1BD9], "color": 0x7AB, "amount": 0},
                }
            },
            "fishing": {
                "title": "Fishing",
                "items": {
                    "Fish": {"type": [0x09CC, 0x09CD, 0x09CE], "color": 0x000, "amount": 0},
                    "Pearl": {"type": 0x3196, "amount": 0},  # Pearls have various colors
                    "Crab": {"type": 0x09B7, "amount": 0},
                    "Lobster": {"type": 0x09B8, "amount": 0},
                    "Shrimp": {"type": 0x09B9, "amount": 0},
                }
            }
        }
        
        # Initialize with the specified resource type
        if resource_type not in self.resource_configs:
            Utils.debug(f"❌ Unknown resource type for tracker: {resource_type}")
            resource_type = "mining"
        
        self.current_config = self.resource_configs[resource_type]
    
    def set_resource_type(self, resource_type):
        """Change the resource type being tracked"""
        if resource_type in self.resource_configs:
            self.resource_type = resource_type
            self.current_config = self.resource_configs[resource_type]
            Utils.debug(f"📊 Resource Tracker: {resource_type} ")
        else:
            Utils.debug(f"❌ Unknown resource type: {resource_type}")
    
    def add_resource_type(self, resource_type, title, items):
        """Add a new resource type configuration"""
        self.resource_configs[resource_type] = {
            "title": title,
            "items": items
        }
        Utils.debug(f"➕ Added new resource type: {resource_type}")
    
    def update_counts(self, item):
        """Update resource counts with given item"""
        item_color = int(GetColor(item))
        item_quantity = GetQuantity(item)
        item_type = GetType(item)
        
        # Check each resource in config
        for resource_name, info in self.current_config["items"].items():
            # Check if item type matches (handle both single type and list of types)
            if "type" in info:
                type_matches = False
                if isinstance(info["type"], list):
                    # Check if item type is in the list
                    type_matches = item_type in info["type"]
                else:
                    # Check if item type matches exactly
                    type_matches = info["type"] == item_type
                
                if type_matches:
                    # Check if color matches, if color is 0xFFFF (any color fits), or if color is omitted
                    if "color" not in info or info["color"] == 0xFFFF or info["color"] == item_color:
                        info["amount"] += item_quantity
                        Utils.debug(f"{resource_name}: +{item_quantity}")
                        return
            # If no type specified, check by color only
            elif "color" in info and info["color"] == item_color:
                info["amount"] += item_quantity
                Utils.debug(f"{resource_name}: +{item_quantity}")
                return
    
    def calculate_counts(self):
        """Generate resource count report"""
        total = 0
        elapsed_time = time.time() - self.start_time
        elapsed_time_readable = str(datetime.timedelta(seconds=int(elapsed_time)))
        
        report = (f"-----------------------\n"
                  f"{self.current_config['title']} pace: {elapsed_time_readable}\n")
        
        for resource_name, info in self.current_config["items"].items():
            total += info["amount"]
            resources_per_hour = info["amount"] / (elapsed_time / 3600)
            report += f"{resource_name}: {info['amount']} / ph: {int(resources_per_hour)}\n"
        
        total_per_hour = total / (elapsed_time / 3600)
        report += (f"Total {self.current_config['title'].lower()} per hour: {int(total_per_hour)}\n"
                   f"-----------------------\n")
        return report


class Discord:
    """Handles Discord webhook notifications with embeds"""
    
    def __init__(self, webhook: str, botname: str = "Resource Bot",
                 avatar: str = "https://i.pinimg.com/originals/87/67/11/876711e56a0ef942cbb2f15844235f2e.jpg"):
        self.webhook, self.botname, self.avatar = webhook, botname, avatar

    def get_resource_name(self, key: str) -> str:
        """Format keys into user-friendly labels (no hardcoded map)."""
        return Utils.format_label(key)

    def send_report(self, title: str, *data):
        """Send formatted report with embeds"""
        try:
            from urllib.request import Request, urlopen
            
            # Create embed structure
            embed = {
                "title": title,
                "color": 0x00ff00,  # Green color
                "fields": [],
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Add fields for each data dictionary
            for arg in data:
                for key in arg.keys():
                    is_last = (key == list(arg.keys())[-1])
                    field = {
                        "name": self.get_resource_name(key),
                        "value": str(arg[key]),
                        "inline": not is_last  # Last field spans full width
                    }
                    embed["fields"].append(field)
            
            # Create webhook payload
            payload = {
                "username": self.botname,
                "avatar_url": self.avatar,
                "embeds": [embed]
            }
            
            # Send webhook
            data = json.dumps(payload).encode('utf-8')
            req = Request(self.webhook, data, headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'
            })
            urlopen(req).read()
            
        except Exception as e:
            AddToSystemJournal("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            AddToSystemJournal("Failed to send report data")
            AddToSystemJournal(f"Error: {str(e)}")
            AddToSystemJournal("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    def send_message(self, message: str):
        """Legacy method for backward compatibility"""
        self.send_report("Resource Report", {"message": message})


class ResourceBot:
    """
    Universal resource gathering bot that orchestrates all components.
    
    This class serves as the main controller for the resource gathering system,
    coordinating between different specialized components like tile scanning,
    TSP optimization, travel management, and resource tracking.
    
    Attributes:
        utils (Utils): Universal game utility functions
        tile_scanner (TileScanner): Handles tile detection and scanning
        tsp_optimizer (TSPOptimizer): Manages route optimization and caching
        travel_manager (TravelManager): Handles runebook travel operations
        inventory_manager (InventoryManager): Manages inventory and crafting
        resource_gatherer (ResourceGatherer): Performs resource gathering operations
        resource_tracker (ResourceTracker): Tracks gathered resources
        discord (Discord): Handles Discord notifications
        stats (dict): Performance and operation statistics
        start_time (float): Script start timestamp
        home_books (List): List of home runebooks for returning to base
    """
    
    def __init__(self):
        self.start_time = time.time()
        self.last_discord_message = time.time()  # Track last Discord message time
        self.stats = {
            'runs_completed': 0,
            'total_travels': 0,
            'total_gathering_attempts': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'tools_crafted': {
                'shovels': 0,
                'hatchets': 0,
                'fishing_poles': 0,
                'tinkering_tools': 0
            },
            'materials_used': {
                'iron_ingots': 0,
                'boards': 0
            }
        }
        self.utils = Utils()
        self.coord_manager = CoordinateManager()
        self.tile_scanner = TileScanner()
        self.tsp_optimizer = TSPOptimizer(self.coord_manager)
        self.travel_manager = TravelManager()
        self.inventory_manager = InventoryManager()
        self.resource_gatherer = ResourceGatherer(self.coord_manager)
        self.resource_tracker = ResourceTracker("mining")  # Default to mining
        self.discord = Discord(DISCORD_WEBHOOK)
        
        self.ore_books = []
        self.home_books = []
    
    def perform_diagnostic_checks(self, resource_type="mining"):
        """Perform startup diagnostic checks based on resource type"""
        try:
            if not Connected():
                Connect()
                Wait(2000)

            print("==============")
            self.utils.check(Connected(), "CLIENT CONNECTED")
            self.utils.check(not Dead(), "CHARACTER ALIVE")

            UseObject(Backpack())
            Wait(1000)

            # Check for appropriate resource book based on resource type
            if resource_type == "mining":
                resource_book_name = ORE_BOOK_NAME
                tool_to_check = SHOVEL
            elif resource_type == "lumberjacking":
                resource_book_name = LUMBER_BOOK_NAME
                tool_to_check = HATCHET
            elif resource_type == "fishing":
                resource_book_name = FISHING_BOOK_NAME
                tool_to_check = FISHING_POLE
            else:
                Utils.log_error(ValueError(f"Unknown resource type: {resource_type}"), "ResourceBot.perform_diagnostic_checks")
                return

            self.utils.check(len(self.travel_manager.find_runebooks_by_name(resource_book_name)) > 0, f"{resource_type.upper()} BOOK NAME FOUND")
            self.utils.check(len(self.travel_manager.find_runebooks_by_name(HOME_BOOK_NAME)) > 0, "HOME BOOK NAME FOUND")
            self.utils.check(Count(TINKER_TOOL) > 0, "TOOLS TINKER FOUND")
            self.utils.check(Count(tool_to_check) > 0, f"TOOLS {resource_type.upper()} FOUND")

            print("==============")
            self.utils.debug("STARTING")
            print("==============")

        except Exception as e:
            print(f"An error occurred: {e}")
            exit()
    
    def run(self, resource_type="mining"):
        """Main resource gathering loop - supports mining, lumberjacking, fishing"""
        self.perform_diagnostic_checks(resource_type)
        
        # Set resource type for tracking
        self.resource_tracker.set_resource_type(resource_type)
        
        # Get appropriate books, scan radius, and waypoint distance based on resource type
        if resource_type == "mining":
            resource_books = self.travel_manager.find_runebooks_by_name(ORE_BOOK_NAME)
            scan_radius = MINING_SCAN_RADIUS
            waypoint_distance = MINING_WAYPOINT_DISTANCE
            tiles = self.tile_scanner.caves
        elif resource_type == "lumberjacking":
            resource_books = self.travel_manager.find_runebooks_by_name(LUMBER_BOOK_NAME)
            scan_radius = LUMBERJACKING_SCAN_RADIUS
            waypoint_distance = LUMBERJACKING_WAYPOINT_DISTANCE
            tiles = TREES
        elif resource_type == "fishing":
            resource_books = self.travel_manager.find_runebooks_by_name(FISHING_BOOK_NAME)
            scan_radius = FISHING_SCAN_RADIUS
            waypoint_distance = FISHING_WAYPOINT_DISTANCE
            tiles = WATER_TILES
        else:
            Utils.log_error(ValueError(f"Unknown resource type: {resource_type}"), "ResourceBot.run")
            return
        
        self.home_books = self.travel_manager.find_runebooks_by_name(HOME_BOOK_NAME)

        while True:
            self.resource_gatherer.visited_waypoints = []
            
            for book_index, resource_book in enumerate(resource_books, 1):
                rune_number = 1
                while rune_number <= 16:  # runebook has 16 runes
                    # Increment travel counter
                    self.stats['total_travels'] += 1
                    
                    self.travel_manager.runebook(resource_book, TRAVEL_METHOD, rune_number, f"{resource_type.title()}", book_index)

                    dataset, dataset_steps, dataset_time = self.tsp_optimizer.cached_adapted_tsp_algorithm(
                        self.tile_scanner.get_tiles(scan_radius, tiles), 
                        self.tsp_optimizer.two_opt_tsp
                    )

                    gathering_successful = self.resource_gatherer.gather(resource_type, dataset, resource_book, rune_number, waypoint_distance, self.stats)
                    
                    if not gathering_successful:
                        # Increment runs completed counter
                        self.stats['runs_completed'] += 1
                        
                        # Use the first home book (index 1)
                        home_book_index = 1
                        self.travel_manager.runebook(self.home_books[0], TRAVEL_METHOD, HOME_NUMBER, f"{HOME_BOOK_NAME}", home_book_index)
                        self.inventory_manager.unload(self.resource_tracker)
                        self.inventory_manager.upload(self.resource_tracker, self.stats)
                        self.inventory_manager.unload(self.resource_tracker)
                        
                        stats = self.resource_tracker.calculate_counts()
                        
                        # Check if we should send Discord message
                        current_time = time.time()
                        should_send_discord = (
                            DISCORD_WEBHOOK.startswith("https://discord.com") and
                            (DISCORD_MESSAGE_INTERVAL == 0 or 
                             current_time - self.last_discord_message >= DISCORD_MESSAGE_INTERVAL * 60)
                        )
                        
                        if should_send_discord:
                            # Get resource counts for Discord embed
                            resource_counts = {}
                            total_ores = 0
                            total_gems = 0
                            elapsed_time = current_time - self.resource_tracker.start_time
                            
                            # Define ore and gem lists for mining
                            ore_types = ["Iron", "Shadow", "Copper", "Bronze", "Gold", "Agapite", "Verite", "Valorite"]
                            gem_types = ["Amethyst", "Citrine", "Diamond", "Emerald", "Ruby", "Sapphire", "Star Sapphire", "Tourmaline"]
                            
                            for resource_name, info in self.resource_tracker.current_config["items"].items():
                                if info["amount"] > 0:  # Only include items with counts > 0
                                    resources_per_hour = info["amount"] / (elapsed_time / 3600)
                                    resource_counts[resource_name] = f"{info['amount']} ({int(resources_per_hour)}/h)"
                                    
                                    # Categorize resources
                                    if resource_name in ore_types:
                                        total_ores += info["amount"]
                                    elif resource_name in gem_types:
                                        total_gems += info["amount"]
                            
                            # Add session statistics
                            session_stats = {
                                "Session Time": str(datetime.timedelta(seconds=int(elapsed_time))),
                                "Total Ores": f"{total_ores} ({int(total_ores / (elapsed_time / 3600))}/h)",
                                "Total Gems": f"{total_gems} ({int(total_gems / (elapsed_time / 3600))}/h)",
                                "Runs Completed": self.stats['runs_completed'],
                                "Total Travels": self.stats['total_travels'],
                                "Gathering Attempts": self.stats['total_gathering_attempts']
                            }
                            
                            # Send Discord report with resource counts and session stats
                            self.discord.send_report(f"{CharName()} {RESOURCE_TYPE.title()} Stats", resource_counts, session_stats)
                            self.last_discord_message = current_time
                        else:
                            print(stats)
                    else:
                        rune_number += 1


# ===== MAIN EXECUTION =====
def main():
    """Main execution function with comprehensive error handling"""
    try:
        # Validate configuration before starting
        valid_travel_methods = ["magery", "chiva", "charges", "gate"]
        Utils.check(TRAVEL_METHOD in valid_travel_methods, f"TRAVEL_METHOD '{TRAVEL_METHOD}' is valid")
        Utils.check(1 <= MINING_SCAN_RADIUS <= 200, f"MINING_SCAN_RADIUS {MINING_SCAN_RADIUS} is between 1-200")
        Utils.check(1 <= LUMBERJACKING_SCAN_RADIUS <= 200, f"LUMBERJACKING_SCAN_RADIUS {LUMBERJACKING_SCAN_RADIUS} is between 1-200")
        Utils.check(1 <= FISHING_SCAN_RADIUS <= 200, f"FISHING_SCAN_RADIUS {FISHING_SCAN_RADIUS} is between 1-200")
        Utils.check(MINING_WAYPOINT_DISTANCE >= 0, f"MINING_WAYPOINT_DISTANCE {MINING_WAYPOINT_DISTANCE} is >= 0")
        Utils.check(LUMBERJACKING_WAYPOINT_DISTANCE >= 0, f"LUMBERJACKING_WAYPOINT_DISTANCE {LUMBERJACKING_WAYPOINT_DISTANCE} is >= 0")
        Utils.check(FISHING_WAYPOINT_DISTANCE >= 0, f"FISHING_WAYPOINT_DISTANCE {FISHING_WAYPOINT_DISTANCE} is >= 0")
        Utils.check(1 <= HOME_NUMBER <= 16, f"HOME_NUMBER {HOME_NUMBER} is between 1-16")
        
        # Initialize and run the bot
        bot = ResourceBot()
        bot.run(RESOURCE_TYPE)
        
    except KeyboardInterrupt:
        Utils.log_warning("Script interrupted by user")
        print("\n🛑 Script stopped by user")
        
    except Exception as e:
        Utils.log_error(e, "Main execution")
        print(f"\n💥 Script crashed: {str(e)}")
        if DEBUG_MODE:
            import traceback
            print(f"📋 Full error: {traceback.format_exc()}")
        
    finally:
        # Print final statistics
        elapsed_time = time.time() - bot.start_time if 'bot' in locals() else 0
        elapsed_readable = str(datetime.timedelta(seconds=int(elapsed_time)))
        
        print("\n" + "="*50)
        print("📊 FINAL STATISTICS")
        print("="*50)
        if 'bot' in locals():
            # Get cache statistics from TSP optimizer
            cache_stats = bot.tsp_optimizer.get_cache_stats()
            bot.stats['cache_hits'] = cache_stats['cache_hits']
            bot.stats['cache_misses'] = cache_stats['cache_misses']
            
            print(f"⏱️ Total Runtime: {elapsed_readable}")
            print(f"🔄 Runs Completed: {bot.stats['runs_completed']}")
            print(f"🚀 Total Travels: {bot.stats['total_travels']}")
            print(f"⛏️ Gathering Attempts: {bot.stats['total_gathering_attempts']}")
            print(f"📋 Cache Hits: {bot.stats['cache_hits']}")
            print(f"🔄 Cache Misses: {bot.stats['cache_misses']}")
            if bot.stats['cache_hits'] + bot.stats['cache_misses'] > 0:
                cache_efficiency = (bot.stats['cache_hits'] / (bot.stats['cache_hits'] + bot.stats['cache_misses'])) * 100
                print(f"📈 Cache Efficiency: {cache_efficiency:.1f}%")
            
            # Crafting statistics - only show items that were actually crafted
            crafted_items = {k: v for k, v in bot.stats['tools_crafted'].items() if v > 0}
            if crafted_items:
                print(f"\n🔨 CRAFTING STATISTICS:")
                for item, count in crafted_items.items():
                    print(f"   {item.title()}: {count}")
            
            # Materials used - only show materials that were actually used
            used_materials = {k: v for k, v in bot.stats['materials_used'].items() if v > 0}
            if used_materials:
                print(f"\n📦 MATERIALS USED:")
                for material, count in used_materials.items():
                    print(f"   {material.replace('_', ' ').title()}: {count}")
            
            # Blacklist statistics
            blacklist_stats = bot.resource_gatherer.get_blacklist_stats()
            if blacklist_stats['total_blacklisted'] > 0:
                print(f"\n🚫 BLACKLIST STATISTICS:")
                print(f"   Total Blacklisted Coordinates: {blacklist_stats['total_blacklisted']}")
                print(f"   Blacklist File: resource_blacklist.json")
        print("="*50)
        print("👋 Script execution ended")

if __name__ == "__main__":
    main()
