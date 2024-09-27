class AutoFunctionsController:
    def __init__(self, state):
        self.state = state
        self.auto_functions_enabled = False

    def toggle_all_auto_functions(self):
        self.auto_functions_enabled = not self.auto_functions_enabled
        self.set_all_auto_functions_state(self.auto_functions_enabled)
        return self.auto_functions_enabled

    def add_auto_function(self, name, function):
        self.state.auto_functions[name] = function
        self.state.update_auto_functions(self.state.auto_functions)

    def remove_auto_function(self, name):
        if name in self.state.auto_functions:
            del self.state.auto_functions[name]
            self.state.update_auto_functions(self.state.auto_functions)

    def get_auto_functions(self):
        return self.state.auto_functions

    def set_all_auto_functions_state(self, enabled):
        for auto_function in self.state.auto_functions.values():
            auto_function['enabled'] = enabled

    # Add other auto function-related methods