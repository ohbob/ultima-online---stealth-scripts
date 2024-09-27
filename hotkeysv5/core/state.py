class State:
    def __init__(self):
        self.hotkeys = {}
        self.friends = []
        self.pets = []
        self.scripts = {}
        self.auto_functions = {}
        self.discovered_functions = {}
        self.flattened_functions = {}
        self.hotkeys_enabled = True
        self.loop_enabled = False
        self.auto_functions_enabled = False
        self.scripts_timeout = 1000
        self.auto_functions_timeout = 1000

    def update_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys
        print(f"Hotkeys updated: {self.hotkeys}")

    def update_friends(self, friends):
        self.friends = friends
        print(f"Friends updated: {self.friends}")

    def update_pets(self, pets):
        self.pets = pets
        print(f"Pets updated: {self.pets}")

    def update_scripts(self, scripts):
        self.scripts = scripts
        print(f"Scripts updated: {self.scripts}")

    def update_auto_functions(self, auto_functions):
        self.auto_functions = auto_functions
        print(f"Auto functions updated: {self.auto_functions}")

    def update_discovered_functions(self, discovered_functions):
        self.discovered_functions = discovered_functions
        self.flattened_functions = self.flatten_discovered_functions(discovered_functions)
        print(f"Discovered functions updated: {self.discovered_functions}")

    def flatten_discovered_functions(self, discovered_functions):
        flattened = {}
        for category, functions in discovered_functions.items():
            for func_name, func_data in functions.items():
                flattened[func_name] = func_data
        return flattened

    def set_hotkeys_enabled(self, enabled):
        self.hotkeys_enabled = enabled
        print(f"Hotkeys {'enabled' if enabled else 'disabled'}")

    def set_loop_enabled(self, enabled):
        self.loop_enabled = enabled
        print(f"Loop {'enabled' if enabled else 'disabled'}")

    def set_auto_functions_enabled(self, enabled):
        self.auto_functions_enabled = enabled
        print(f"Auto functions {'enabled' if enabled else 'disabled'}")

    def set_scripts_timeout(self, timeout):
        self.scripts_timeout = timeout
        print(f"Scripts timeout set to {timeout} ms")

    def set_auto_functions_timeout(self, timeout):
        self.auto_functions_timeout = timeout
        print(f"Auto functions timeout set to {timeout} ms")

    # Add other state-related methods