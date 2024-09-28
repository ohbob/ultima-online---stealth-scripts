from pynput import keyboard
from threading import Thread

class HotkeyController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.hotkeys = {}
        self.listener = None
        self.is_running = False
        self.current_keys = set()

    def setup_hotkey(self, hotkey, func_name):
        self.hotkeys[self.parse_hotkey(hotkey)] = func_name
        print(f"Hotkey set: {hotkey} for function {func_name}")

    def clear_hotkey(self, hotkey):
        parsed_hotkey = self.parse_hotkey(hotkey)
        if parsed_hotkey in self.hotkeys:
            del self.hotkeys[parsed_hotkey]
            print(f"Hotkey cleared: {hotkey}")

    def parse_hotkey(self, hotkey):
        return frozenset(part.lower() for part in hotkey.split('+'))

    def on_press(self, key):
        try:
            if isinstance(key, keyboard.Key):
                self.current_keys.add(key.name.lower())
            else:
                self.current_keys.add(key.char.lower())
            
            current_hotkey = frozenset(self.current_keys)
            if current_hotkey in self.hotkeys:
                func_name = self.hotkeys[current_hotkey]
                print(f"Hotkey pressed: {'+'.join(sorted(current_hotkey))} - Running function: {func_name}")
                self.main_controller.run_once(func_name)
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if isinstance(key, keyboard.Key):
                self.current_keys.discard(key.name.lower())
            else:
                self.current_keys.discard(key.char.lower())
        except AttributeError:
            pass

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.listener.start()
            print("Hotkey listener started")

    def stop(self):
        if self.is_running:
            self.is_running = False
            if self.listener:
                self.listener.stop()
                self.listener = None
            print("Hotkey listener stopped")

    def get_hotkeys(self):
        return {'+'.join(sorted(k)): v for k, v in self.hotkeys.items()}

    def set_hotkeys(self, hotkeys):
        self.hotkeys = {self.parse_hotkey(k): v for k, v in hotkeys.items()}
        print(f"Hotkeys set: {self.hotkeys}")