from enum import Enum
from typing import NewType, Optional
from py_stealth import *
from datetime import datetime, timedelta

# Constants
VENDOR_CONTEXT_MENU = 1
BOD_TYPE = 0x2258
WAIT_TIME = 700
WAIT_LAG_TIME = 5000
BOOK_LIMIT = 500
BOD_INTERVAL = timedelta(minutes=60)  # 60 minutes interval
BOD_GUMP_ID = 2611865322
LUNA_COORDINATES = (986, 519)

VendorID = NewType('VendorID', int)
ColorCode = NewType('ColorCode', int)
ItemID = NewType('ItemID', int)
GumpID = NewType('GumpID', int)


class BodType(Enum):
    BLACKSMITH = {"bod_book_name": "BS", 'vendor': 0x0009B4F7, 'bod_color': 0x44e}
    TAILORING = {"bod_book_name": "TS", 'vendor': 0x0009B52C, 'bod_color': 0x483}


class Profile:
    def __init__(self, name: str, bod_type: BodType, active: bool = True):
        self.name = name
        self.active = active
        self.bod_type = bod_type
        self.last_time = datetime.now() - timedelta(days=1)
        self.vendor = bod_type.value['vendor']

    def __str__(self) -> str:
        return self.name

    def can_get_bod(self) -> bool:
        time_since_last_bod = datetime.now() - self.last_time
        time_left = BOD_INTERVAL - time_since_last_bod

        if time_left > timedelta(minutes=0):
            minutes_left = time_left.seconds // 60
            print(f"{minutes_left} minutes left to get a bod {self.name}")
            return False
        return True

    def should_connect(self) -> bool:
        return datetime.now() - self.last_time >= timedelta(minutes=1)


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


def load_profile(profile: Profile):
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


def get_bod(profile: Profile) -> bool:
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

    # Parse journal for relevant information
    while index < HighJournal():
        index = index + 1
        line = Journal(index)
        if LineID() == profile.vendor:
            minutes_left = int(line.split("available in about ")[1].split(" minutes.")[0])
            print(f"Bod available in {minutes_left} minutes for {profile.name}")
            profile.last_time = datetime.now() - timedelta(minutes=(60 - minutes_left))
            break

    return False


def find_bod_book(name: str) -> Optional[ItemID]:
    CheckLag(60000)
    FindTypeEx(0x2259, 0xFFFF, Backpack())
    for item in GetFoundList():
        try:
            for _ in range(3):  # Try to get the tooltip 3 times
                tool = GetTooltip(item)
                if "Name: " in tool:
                    item_name = tool.split("Name: ")
                    # Ensure there is a name part after splitting and it matches the desired name
                    if len(item_name) > 0 and name == item_name[1]:
                        return item
        except Exception as e:
            # Log or handle the error as needed
            print(f"Error processing item {item}: {e}")
    print(f"No BOD book found with the name {name}")
    return None


def bod_book_deeds_count(bookid: ItemID) -> int:
    CheckLag(60000)
    tool = GetTooltip(bookid)
    count = 0
    if "Deeds in book: " in tool:
        try:
            # Attempt to extract and convert the count to an integer
            count_str = tool.split("Deeds in book: ")[1].split("|")[0]
            count = int(count_str)
        except ValueError:
            # Handle the case where conversion to integer fails
            print(f"Could not convert '{count_str}' to an integer.")
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error: {e}")
    return count


def process_profiles(_profiles):
    while True:
        for profile in _profiles:
            if profile.active:
                if profile.can_get_bod():
                    load_profile(profile)
                    mybook = find_bod_book(profile.bod_type.value['bod_book_name'])
                    # Check if mybook is not None before proceeding
                    if mybook is None:
                        print(f"Book not found for profile {profile.name}. Skipping...")
                        continue  # Skip to the next profile if the book is not found

                    if bod_book_deeds_count(mybook) >= BOOK_LIMIT:
                        profile.active = False
                        continue  # Skip to the next profile if the book limit is reached

                    get_bod(profile)

                    if FindTypeEx(BOD_TYPE, profile.bod_type.value['bod_color'], Backpack()):
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


if __name__ == "__main__":
    profiles = [
        Profile("BBQ", BodType.BLACKSMITH)
    ]
    process_profiles(profiles)
