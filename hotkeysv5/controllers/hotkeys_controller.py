class HotkeysController:
    def __init__(self, state):
        self.state = state
        self.hotkeys = {}

    def add_hotkey(self, function_name, hotkey):
        self.hotkeys[function_name] = hotkey
        self.state.update_hotkeys(self.hotkeys)

    def remove_hotkey(self, function_name):
        if function_name in self.hotkeys:
            del self.hotkeys[function_name]
            self.state.update_hotkeys(self.hotkeys)

    def get_hotkeys(self):
        return self.hotkeys

    # Add other hotkey-related methods