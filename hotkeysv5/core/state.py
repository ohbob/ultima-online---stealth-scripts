class State:
    def __init__(self):
        self.discovered_functions = {}
        self.auto_functions = {}
        self.hotkeys = {}
        self.friends = []
        self.pets = []
        self.scripts = {}  # Add this line
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
        # Add any additional logic for updating pets state
        print(f"Pets updated: {self.pets}")

    def update_scripts(self, scripts):
        self.scripts = scripts
        print(f"Scripts updated: {list(self.scripts.keys())}")

    def update_auto_functions(self, auto_functions):
        self.auto_functions = auto_functions
        print(f"Auto functions updated: {self.auto_functions.keys()}")

    def update_discovered_functions(self, discovered_functions):
        self.discovered_functions = discovered_functions
        print(f"Discovered functions updated: {self.discovered_functions.keys()}")

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

    def print_discovered_functions(self):
        print("\nDiscovered Functions:")
        for category, functions in self.discovered_functions.items():
            print(f"\n{category}:")
            for func_name, func_data in functions.items():
                print(f"  - {func_name}")
                # if 'description' in func_data:
                #     print(f"    Description: {func_data['description']}")
                # if 'hotkey' in func_data:
                #     print(f"    Hotkey: {func_data['hotkey']}")

        print("\nAuto Functions:")
        for category, functions in self.auto_functions.items():
            print(f"\n{category}:")
            for func_name, func_data in functions.items():
                print(f"  - {func_name}")
                # if 'description' in func_data:
                #     print(f"    Description: {func_data['description']}")
                # if 'hotkey' in func_data:
                #     print(f"    Hotkey: {func_data['hotkey']}")

    # Add other state-related methods