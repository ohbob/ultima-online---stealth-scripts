class AutoFunctionsController:
    def __init__(self, state):
        self.state = state

    def set_all_auto_functions_state(self, enabled):
        pass
        # for category in self.state.auto_functions.values():
        #     for func_data in category.values():
        #         func_data['enabled'] = enabled

    def toggle_auto_function(self, func_name, enabled):
        for category, functions in self.state.auto_functions.items():
            if func_name in functions:
                functions[func_name]['enabled'] = enabled
                break
        print(f"{'Enabled' if enabled else 'Disabled'} auto function: {func_name}")

    # Add other auto function-related methods