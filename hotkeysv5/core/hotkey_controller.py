from pynput import keyboard
import logging
import threading

class HotkeyController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.hotkeys = {}
        self.enabled = False
        self.listener = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.pressed_keys = set()
        self.whitelisted_functions = {'ToggleAutoFunctions', 'ToggleHotkeys'}

    def on_press(self, key):
        try:
            char = key.char.lower() if hasattr(key, 'char') and key.char else key.name.lower()
        except AttributeError:
            char = str(key).lower().replace("'", "")

        self.pressed_keys.add(char)
        self.logger.debug(f"Key pressed: {char}")
        self.logger.debug(f"Current pressed keys: {self.pressed_keys}")

        current_hotkey = '+'.join(sorted(self.pressed_keys))
        self.logger.debug(f"Current hotkey: {current_hotkey}")

        if current_hotkey in self.hotkeys:
            func_name = self.hotkeys[current_hotkey]
            self.logger.info(f"Hotkey detected: {current_hotkey} for function: {func_name}")
            if func_name in self.whitelisted_functions or self.enabled:
                self.logger.info(f"Executing hotkey: {current_hotkey} for function: {func_name}")
                threading.Thread(target=self.main_controller.run_once, args=(func_name,)).start()
            else:
                self.logger.info(f"Hotkey not executed: {current_hotkey} for function: {func_name} (not whitelisted and hotkeys disabled)")

    def on_release(self, key):
        try:
            char = key.char.lower() if hasattr(key, 'char') and key.char else key.name.lower()
        except AttributeError:
            char = str(key).lower().replace("'", "")

        self.pressed_keys.discard(char)
        self.logger.debug(f"Key released: {char}")
        self.logger.debug(f"Current pressed keys: {self.pressed_keys}")

    def start(self):
        self.logger.info("Starting hotkey listener")
        if not self.listener:
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
        self.enabled = True
        self.logger.info("Hotkey listener started and enabled")
        self.logger.debug(f"Current hotkeys: {self.hotkeys}")

    def stop(self):
        self.enabled = False
        self.logger.info("Hotkey listener disabled (but still running)")

    def setup_hotkey(self, hotkey, func_name):
        self.hotkeys[hotkey.lower()] = func_name
        self.logger.info(f"Hotkey set: {hotkey} for function {func_name}")
        self.logger.debug(f"Current hotkeys: {self.hotkeys}")

    def get_hotkeys(self):
        return self.hotkeys

    def set_hotkeys(self, hotkeys):
        self.hotkeys = {k.lower(): v for k, v in hotkeys.items()}
        self.logger.info(f"Hotkeys set: {self.hotkeys}")

    def clear_hotkey(self, hotkey):
        if hotkey.lower() in self.hotkeys:
            del self.hotkeys[hotkey.lower()]
            self.logger.info(f"Hotkey cleared: {hotkey}")
        self.logger.debug(f"Current hotkeys: {self.hotkeys}")

    def clear_all_hotkeys(self):
        self.hotkeys.clear()
        self.logger.info("All hotkeys cleared")
        self.logger.debug(f"Current hotkeys: {self.hotkeys}")

    def toggle_all_hotkeys(self):
        self.enabled = not self.enabled
        state = "enabled" if self.enabled else "disabled"
        self.logger.info(f"All hotkeys {state}")
        return self.enabled