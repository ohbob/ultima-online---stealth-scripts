from py_stealth import *

def main(manager):
    manager.pets_tab.add_pet()

def debug(message, level="info"):
    print(f"[{level.upper()}] {message}")