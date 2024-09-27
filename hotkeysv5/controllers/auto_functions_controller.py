class AutoFunctionsController:
    def __init__(self, state):
        self.state = state
        self.auto_functions = {}

    def add_auto_function(self, name, function):
        self.auto_functions[name] = function
        self.state.update_auto_functions(self.auto_functions)

    def remove_auto_function(self, name):
        if name in self.auto_functions:
            del self.auto_functions[name]
            self.state.update_auto_functions(self.auto_functions)

    def get_auto_functions(self):
        return self.auto_functions

    # Add other auto function-related methods