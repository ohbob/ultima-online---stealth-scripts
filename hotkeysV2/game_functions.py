from py_stealth import *
import time
from utils import debug, configurable_function, SystemFunctions

class Functions:
    autoheal_enabled = False
    autoheal_threshold = 95  # Default value, can be changed via config

    @staticmethod
    @configurable_function(enabled=True, threshold=95)
    def heal_self():
        debug("Healing Self", "success")
        # Add actual healing logic here

    @staticmethod
    def hide():
        if not Hidden():
            debug("Not hidden", "warning")
            UseSkill('Hiding')
        else:
            debug("Already hidden", "info")

    @staticmethod
    def cast_magic_arrow():
        debug("Casting Magic Arrow", "info")

    @staticmethod
    def cancel_target():
        if TargetPresent():
            CancelTarget()
            debug("Target Canceled", "warning")

    @staticmethod
    def toggle_autoheal():
        Functions.autoheal_enabled = not Functions.autoheal_enabled
        debug(f"Autoheal {'enabled' if Functions.autoheal_enabled else 'disabled'}", 
              "success" if Functions.autoheal_enabled else "fail")

def main_loop():
    while True:
        if SystemFunctions.hotkeys_enabled:
            if Functions.autoheal_enabled:
                if GetHP(Self()) < MaxHP():
                    Functions.heal_self()
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage