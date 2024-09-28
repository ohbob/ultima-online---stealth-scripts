from py_stealth import *
import time
from hotkey_config import debug, configurable_function, SystemFunctions

# Global variables
autoheal_enabled = False
autoheal_threshold = 95  # Default value, can be changed via config

@configurable_function(enabled=True, threshold=95)
def heal_self():
    debug("Healing Self", "success")
    # Add actual healing logic here

def hide():
    if not Hidden():
        debug("Not hidden", "warning")
        UseSkill('Hiding')
    else:
        debug("Already hidden", "info")

def cast_magic_arrow():
    debug("Casting Magic Arrow", "info")

def cancel_target():
    if TargetPresent():
        CancelTarget()
        debug("Target Canceled", "warning")

def toggle_autoheal():
    global autoheal_enabled
    autoheal_enabled = not autoheal_enabled
    debug(f"Autoheal {'enabled' if autoheal_enabled else 'disabled'}", 
          "success" if autoheal_enabled else "fail")

def main_loop():
    while True:
        if SystemFunctions.hotkeys_enabled:
            if autoheal_enabled:
                if GetHP(Self()) < MaxHP():
                    heal_self()
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage