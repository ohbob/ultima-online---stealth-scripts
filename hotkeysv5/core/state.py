class State:
    def __init__(self):
        self.hotkeys = {}
        self.friends = []
        self.pets = []
        self.scripts = {}
        self.auto_functions = {}

    def update_hotkeys(self, hotkeys):
        self.hotkeys = hotkeys

    def update_friends(self, friends):
        self.friends = friends

    def update_pets(self, pets):
        self.pets = pets

    def update_scripts(self, scripts):
        self.scripts = scripts

    def update_auto_functions(self, auto_functions):
        self.auto_functions = auto_functions

    # Add other state-related methods