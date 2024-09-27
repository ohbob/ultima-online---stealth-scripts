class HotkeysController:
    def __init__(self, state):
        self.state = state
        self.all_hotkeys_enabled = True

    def add_hotkey(self, function_name, hotkey):
        self.hotkeys[function_name] = hotkey
        self.state.update_hotkeys(self.hotkeys)

    def remove_hotkey(self, function_name):
        if function_name in self.hotkeys:
            del self.hotkeys[function_name]
            self.state.update_hotkeys(self.hotkeys)

    def get_hotkeys(self):
        return self.hotkeys

    def toggle_all_hotkeys(self):
        self.all_hotkeys_enabled = not self.all_hotkeys_enabled
        for hotkey in self.state.hotkeys.values():
            hotkey['enabled'] = self.all_hotkeys_enabled
        return self.all_hotkeys_enabled

    def set_all_hotkeys_state(self, enabled):
        for hotkey in self.state.hotkeys.values():
            hotkey['enabled'] = enabled

    # Add other hotkey-related methods