from py_stealth import *
from utils import debug
from hotkey_config import HotkeyConfig

def main(config):
    friends = config.get_friends_list()
    pets = config.get_pets_list()

    debug("Friends list:", "info")
    for friend_id, friend_name in friends:
        debug(f"ID: {friend_id}, Name: {friend_name}", "info")

    debug("\nPets list:", "info")
    for pet_id, pet_name in pets:
        debug(f"ID: {pet_id}, Name: {pet_name}", "info")