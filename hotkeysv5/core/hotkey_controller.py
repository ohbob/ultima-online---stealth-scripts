from pynput import keyboard
import logging
import threading

class HotkeyController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.hotkeys = {}
        self.whitelisted_hotkeys = {}
        self.listener = None
        self.is_running = False
        self.current_keys = set()
        self.logger = logging.getLogger(__name__)
        self.stop_event = threading.Event()
        self.whitelisted_functions = {'ToggleHotkeys', 'ToggleAutoFunctions'}

    def on_press(self, key):
        self.logger.debug(f"Key pressed: {key}")
        if isinstance(key, keyboard.Key):
            self.current_keys.add(key.name.lower())
        elif isinstance(key, keyboard.KeyCode):
            if key.char:
                self.current_keys.add(key.char.lower())
            elif key.vk:
                self.current_keys.add(chr(key.vk).lower())

        current_hotkey = frozenset(self.current_keys)
        self.logger.debug(f"Current keys: {current_hotkey}")

        # Always check for whitelisted hotkeys
        if current_hotkey in self.whitelisted_hotkeys:
            func_name = self.whitelisted_hotkeys[current_hotkey]
            self.logger.info(f"Whitelisted hotkey detected: {'+'.join(sorted(current_hotkey))} - Function: {func_name}")
            threading.Thread(target=self.main_controller.run_once, args=(func_name,)).start()
        elif self.is_running and current_hotkey in self.hotkeys:
            func_name = self.hotkeys[current_hotkey]
            self.logger.info(f"Hotkey detected: {'+'.join(sorted(current_hotkey))} - Function: {func_name}")
            threading.Thread(target=self.main_controller.run_once, args=(func_name,)).start()

    def on_release(self, key):
        try:
            if isinstance(key, keyboard.KeyCode) and key.char:
                self.current_keys.discard(key.char.lower())
            elif isinstance(key, keyboard.Key):
                self.current_keys.discard(key.name.lower())
        except AttributeError:
            pass

    def start(self):
        if not self.listener:
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
        self.is_running = True
        self.logger.info("Hotkey listener started")

    def stop(self):
        pass
        # self.is_running = False
        # self.logger.info("Hotkey listener stopped (non-whitelisted hotkeys disabled)")

    def setup_hotkey(self, hotkey, func_name):
        parsed_hotkey = self.parse_hotkey(hotkey)
        if func_name in self.whitelisted_functions:
            self.whitelisted_hotkeys[parsed_hotkey] = func_name
        else:
            self.hotkeys[parsed_hotkey] = func_name
        self.logger.info(f"Hotkey set: {hotkey} for function {func_name}")

    def parse_hotkey(self, hotkey):
        return frozenset(part.lower() for part in hotkey.split('+'))

    def get_hotkeys(self):
        all_hotkeys = {**self.hotkeys, **self.whitelisted_hotkeys}
        return {'+'.join(sorted(k)): v for k, v in all_hotkeys.items()}

    def set_hotkeys(self, hotkeys):
        self.hotkeys = {}
        self.whitelisted_hotkeys = {}
        for hotkey, func_name in hotkeys.items():
            self.setup_hotkey(hotkey, func_name)
        self.logger.info(f"Hotkeys set: {self.get_hotkeys()}")

    def clear_hotkey(self, hotkey):
        parsed_hotkey = self.parse_hotkey(hotkey)
        if parsed_hotkey in self.hotkeys:
            del self.hotkeys[parsed_hotkey]
        elif parsed_hotkey in self.whitelisted_hotkeys:
            del self.whitelisted_hotkeys[parsed_hotkey]
        self.logger.info(f"Hotkey cleared: {hotkey}")

    def clear_all_hotkeys(self):
        self.hotkeys.clear()
        self.whitelisted_hotkeys.clear()
        self.logger.info("All hotkeys cleared")

    def toggle_all_hotkeys(self):
        self.is_running = not self.is_running
        state = "enabled" if self.is_running else "disabled"
        self.logger.info(f"All non-whitelisted hotkeys {state}")
        return self.is_running