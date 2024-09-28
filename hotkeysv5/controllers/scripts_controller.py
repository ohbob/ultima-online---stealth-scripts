class ScriptsController:
    def __init__(self, state):
        self.state = state
        self.scripts = {}

    def add_script(self, name, script):
        self.scripts[name] = script
        self.state.update_scripts(self.scripts)

    def remove_script(self, name):
        if name in self.scripts:
            del self.scripts[name]
            self.state.update_scripts(self.scripts)

    def get_scripts(self):
        return self.scripts

    def run_once(self, func_name):
        # This method should delegate to the MainController's run_script method
        # We'll update the MainController to handle this
        pass

    # Add other script-related methods