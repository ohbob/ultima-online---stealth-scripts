from py_stealth import *
from datetime import datetime, timedelta

# ==============================
# Constants
# ==============================

VENDOR_CONTEXT_MENU = 1
BOD_TYPE = 0x2258
WAIT_TIME = 700
WAIT_LAG_TIME = 5000
BOOK_LIMIT = 500
BOD_INTERVAL = timedelta(minutes=60)
BOD_GUMP_ID = 2611865322
LUNA_COORDINATES = (986, 519)

# Vendor IDs
VENDOR_BLACKSMITH = 0x0009B4F7
VENDOR_TAILORING  = 0x0009B52C

# BOD Book Colors
COLOR_BLACKSMITH = 0x44e
COLOR_TAILORING  = 0x483

# ==============================
# Profiles Lists by Type
# ==============================

PROFILES_BS = ["BBQ"]
PROFILES_TAILOR = ["NIG"]

# ==============================
# Profile Class
# ==============================

class Profile:
    def __init__(self, name, bod_book_name, vendor, bod_color, active=True):
        self.name = name
        self.bod_book_name = bod_book_name
        self.vendor = vendor
        self.bod_color = bod_color
        self.active = active
        self.last_time = datetime.now() - timedelta(days=1)

    def __str__(self):
        return self.name

    def can_get_bod(self):
        time_since_last = datetime.now() - self.last_time
        if time_since_last < BOD_INTERVAL:
            minutes_left = (BOD_INTERVAL - time_since_last).seconds // 60
            print(f"{minutes_left} minutes left for {self.name}")
            return False
        return True

    def should_connect(self):
        return datetime.now() - self.last_time >= timedelta(minutes=1)

# ==============================
# Build Profile Instances
# ==============================

PROFILES = []

for name in PROFILES_BS:
    PROFILES.append(Profile(name, "BS", VENDOR_BLACKSMITH, COLOR_BLACKSMITH))

for name in PROFILES_TAILOR:
    PROFILES.append(Profile(name, "TS", VENDOR_TAILORING, COLOR_TAILORING))

# ==============================
# Utility Functions
# ==============================

def disconnect():
    while Connected():
        Disconnect()
        Wait(WAIT_LAG_TIME)

def connect():
    while not Connected():
        Connect()
        Wait(WAIT_LAG_TIME)

def close_gumps():
    while IsGump():
        if IsGumpCanBeClosed(0):
            CloseSimpleGump(0)
            Wait(WAIT_TIME)

def load_profile(profile):
    if not profile.should_connect():
        print(f"Skipping {profile.name}, as it's too soon to reconnect.")
        return

    print(f"Loading profile {profile} {datetime.now().strftime('%H:%M:%S')}")
    disconnect()
    ChangeProfile(profile.name)
    connect()
    close_gumps()
    UseObject(Backpack())
    Wait(WAIT_TIME)

def get_bod(profile):
    print(f"Requesting bod on {profile}")
    newMoveXYZ(*LUNA_COORDINATES, GetZ(Self()), 0, 1, False, None)
    index = HighJournal()
    SetContextMenuHook(profile.vendor, VENDOR_CONTEXT_MENU)
    Wait(WAIT_TIME)
    RequestContextMenu(profile.vendor)
    Wait(WAIT_TIME)
    CheckLag(60000)

    for i in range(GetGumpsCount()):
        if GetGumpInfo(i)['GumpID'] == BOD_GUMP_ID:
            WaitGump('1')
            CheckLag(50000)
            print("Got bod")
            return True

    while index < HighJournal():
        index += 1
        line = Journal(index)
        if LineID() == profile.vendor:
            try:
                minutes_left = int(line.split("available in about ")[1].split(" minutes.")[0])
                print(f"Bod available in {minutes_left} minutes for {profile.name}")
                profile.last_time = datetime.now() - timedelta(minutes=(60 - minutes_left))
            except Exception:
                print(f"Could not parse wait time for {profile.name} from journal line: {line}")
            break

    return False

def find_bod_book(name):
    CheckLag(60000)
    FindTypeEx(0x2259, 0xFFFF, Backpack())
    for item in GetFoundList():
        try:
            for _ in range(3):  # try 3 times
                tool = GetTooltip(item)
                if "Name: " in tool:
                    parts = tool.split("Name: ")
                    if len(parts) > 1 and name == parts[1]:
                        return item
        except Exception as e:
            print(f"Error processing item {item}: {e}")
    print(f"No BOD book found with the name {name}")
    return None

def bod_book_deeds_count(bookid):
    CheckLag(60000)
    tool = GetTooltip(bookid)
    count = 0
    if "Deeds in book: " in tool:
        try:
            count_str = tool.split("Deeds in book: ")[1].split("|")[0]
            count = int(count_str)
        except Exception as e:
            print(f"Error parsing deeds count: {e}")
    return count

# ==============================
# Main Processing Loop
# ==============================

def process_profiles(profiles):
    while True:
        for profile in profiles:
            if not profile.active:
                continue

            if profile.can_get_bod():
                load_profile(profile)
                mybook = find_bod_book(profile.bod_book_name)
                if mybook is None:
                    print(f"Book not found for profile {profile.name}. Skipping...")
                    continue

                if bod_book_deeds_count(mybook) >= BOOK_LIMIT:
                    print(f"Book limit reached for {profile.name}, deactivating profile.")
                    profile.active = False
                    continue

                if get_bod(profile):
                    if FindTypeEx(BOD_TYPE, profile.bod_color, Backpack()):
                        for item in GetFoundList():
                            print(f"Found bod {item}, moving to book {mybook}")
                            MoveItem(item, 1, mybook, 0, 0, 0)
                            profile.last_time = datetime.now()
                            print(f"Adjusting new wait time for profile {profile.name}")
                            print("---------------------------")
                            Wait(WAIT_TIME)
                            CheckLag(60000)
        disconnect()
        Wait(60000)

# ==============================
# Entry Point
# ==============================

if __name__ == "__main__":
    process_profiles(PROFILES)
