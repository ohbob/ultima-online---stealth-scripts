from py_stealth import *
from typing import Literal

def debug(message: str, color: Literal["success", "fail", "info", "warning"] = "info") -> None:
    color_map = {
        "success": 60,  # Green
        "fail": 30,     # Red
        "info": 5,      # Blue
        "warning": 40   # Orange
    }
    ClientPrintEx(Self(), color_map[color], 1, f"* {message.upper()} *")

def configurable_function(**kwargs):
    def decorator(func):
        func.config = kwargs
        return func
    return decorator

class SystemFunctions:
    hotkeys_enabled = True

    @staticmethod
    def toggle_all_hotkeys():
        SystemFunctions.hotkeys_enabled = not SystemFunctions.hotkeys_enabled
        debug(f"Hotkeys {'enabled' if SystemFunctions.hotkeys_enabled else 'disabled'}", 
              "success" if SystemFunctions.hotkeys_enabled else "fail")