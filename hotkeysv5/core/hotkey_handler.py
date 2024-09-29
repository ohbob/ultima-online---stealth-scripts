import keyboard
import threading

class HotkeyHandler:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.hotkeys = {}
        self.enabled = True
        self.lock = threading.Lock()

    def add_hotkey(self, key, callback):
        with self.lock:
            self.hotkeys[key] = callback
            keyboard.add_hotkey(key, self._safe_callback, args=(key,))

    def remove_hotkey(self, key):
        with self.lock:
            if key in self.hotkeys:
                keyboard.remove_hotkey(key)
                del self.hotkeys[key]

    def _safe_callback(self, key):
        if self.enabled:
            with self.lock:
                if key in self.hotkeys:
                    self.main_controller.run_in_main_thread(self.hotkeys[key])

    def toggle_hotkeys(self, state):
        self.enabled = state

    def clear_all_hotkeys(self):
        with self.lock:
            for key in list(self.hotkeys.keys()):
                self.remove_hotkey(key)

    def get_hotkeys(self):
        with self.lock:
            return dict(self.hotkeys)