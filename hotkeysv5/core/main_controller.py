from controllers.auto_discovery_controller import AutoDiscoveryController
from controllers.hotkeys_controller import HotkeysController
from controllers.friends_controller import FriendsController
from controllers.pets_controller import PetsController
from controllers.scripts_controller import ScriptsController
from controllers.auto_functions_controller import AutoFunctionsController
from core.state import State
import importlib
import sys
import io
from contextlib import redirect_stdout
from core.py_stealth import *
from core.uo_globals import *  # Import the global functions

class MainController:
    def __init__(self, py_stealth):
        self.py_stealth = py_stealth
        self.state = State()
        self.hotkeys_controller = HotkeysController(self.state)
        self.friends_controller = FriendsController(self.state, self.py_stealth)
        self.pets_controller = PetsController(self.state, self.py_stealth)
        self.scripts_controller = ScriptsController(self.state)
        self.auto_functions_controller = AutoFunctionsController(self.state)
        self.auto_discovery_controller = AutoDiscoveryController(self.state)
        self.ui = None
        self.scripts_tab = None  # This will be set when creating the UI
        self.hotkeys_enabled = False  # Initial state
        self.discover_all_functions()

    def set_ui(self, ui):
        self.ui = ui
        if hasattr(ui, 'scripts_tab'):
            self.scripts_tab = ui.scripts_tab
        self.update_ui_with_discovered_functions()  # Update UI after it's set

    def set_hotkey(self, func_name):
        # This should be implemented in the HotkeysController
        self.hotkeys_controller.set_hotkey(func_name)
        print(f"Hotkey set for function: {func_name}")
        self.print_current_state()

    def clear_hotkey(self, func_name):
        # This should be implemented in the HotkeysController
        self.hotkeys_controller.clear_hotkey(func_name)
        print(f"Hotkey cleared for function: {func_name}")
        self.print_current_state()

    def run_once(self, func_name):
        print(f"Running function once: {func_name}")
        self.run_script(func_name, loop=False, timeout=self.state.scripts_timeout)

    def set_scripts_timeout(self, timeout):
        try:
            timeout = int(timeout)
            self.state.set_scripts_timeout(timeout)
            print(f"Scripts timeout set to: {timeout} ms")
            self.print_current_state()
        except ValueError:
            print("Invalid timeout value. Please enter a valid integer.")

    def set_auto_functions_timeout(self, timeout):
        try:
            timeout = int(timeout)
            self.state.set_auto_functions_timeout(timeout)
            print(f"Auto functions timeout set to: {timeout} ms")
            self.print_current_state()
        except ValueError:
            print("Invalid timeout value. Please enter a valid integer.")

    def toggle_all_auto_functions(self):
        new_state = not self.state.auto_functions_enabled
        self.state.set_auto_functions_enabled(new_state)
        self.auto_functions_controller.set_all_auto_functions_state(new_state)
        print(f"Auto functions {'enabled' if new_state else 'disabled'}")
        self.print_current_state()
        if self.ui and hasattr(self.ui, 'auto_functions_tab'):
            self.ui.auto_functions_tab.update_auto_button_state(new_state)
        return new_state

    def toggle_all_hotkeys(self):
        self.hotkeys_enabled = not self.hotkeys_enabled
        # ... logic to enable/disable hotkeys ...
        if self.scripts_tab:
            self.scripts_tab.update_hotkey_button_state(self.hotkeys_enabled)
        return self.hotkeys_enabled

    def save_config(self):
        # Implement saving configuration
        pass

    def load_config(self):
        # Implement loading configuration
        pass

    def discover_all_functions(self):
        print("Starting function discovery...")
        self.auto_discovery_controller.discover_all_functions()
        self.state.print_discovered_functions()
        print("Function discovery complete")

    def update_ui_with_discovered_functions(self):
        if self.ui:
            print("Updating UI with discovered functions...")
            self.ui.scripts_tab.populate_tree()
            self.ui.auto_functions_tab.populate_tree()
        else:
            print("UI not set, skipping UI update")

    def set_hotkeys_state(self, enabled):
        self.state.set_hotkeys_enabled(enabled)
        self.hotkeys_controller.set_all_hotkeys_state(enabled)
        print(f"Hotkeys {'enabled' if enabled else 'disabled'}")
        self.print_current_state()

    def set_loop_state(self, enabled):
        self.state.set_loop_enabled(enabled)
        print(f"Loop {'enabled' if enabled else 'disabled'}")
        self.print_current_state()

    def set_auto_functions_state(self, enabled):
        self.state.set_auto_functions_enabled(enabled)
        self.auto_functions_controller.set_all_auto_functions_state(enabled)
        print(f"Auto functions {'enabled' if enabled else 'disabled'}")
        self.print_current_state()
        if self.ui and hasattr(self.ui, 'auto_functions_tab'):
            self.ui.auto_functions_tab.update_auto_button_state(enabled)

    def print_current_state(self):
        print("\nCurrent Application State:")
        print(f"Hotkeys Enabled: {self.state.hotkeys_enabled}")
        print(f"Loop Enabled: {self.state.loop_enabled}")
        print(f"Auto Functions Enabled: {self.state.auto_functions_enabled}")
        print(f"Scripts Timeout: {self.state.scripts_timeout} ms")
        print(f"Auto Functions Timeout: {self.state.auto_functions_timeout} ms")
        print(f"Number of Hotkeys: {len(self.state.hotkeys)}")
        print(f"Number of Friends: {len(self.state.friends)}")
        print(f"Number of Pets: {len(self.state.pets)}")
        print(f"Number of Discovered Functions: {sum(len(funcs) for funcs in self.state.discovered_functions.values())}")
        print(f"Number of Auto Functions: {sum(len(funcs) for funcs in self.state.auto_functions.values())}")
        print()  # Empty line for better readability

    def get_discovered_functions(self):
        return self.state.discovered_functions

    def get_auto_functions(self):
        return self.state.auto_functions

    def run_script(self, func_name, loop, timeout):
        print(f"Running script: {func_name}")
        print(f"Loop: {'Enabled' if loop else 'Disabled'}")
        print(f"Timeout: {timeout} ms")

        # Find the script file path and function data
        script_path = None
        func_data = None
        for category, functions in self.state.discovered_functions.items():
            if func_name in functions:
                func_data = functions[func_name]
                script_path = func_data.get('path')
                break
        
        if script_path is None:
            for category, functions in self.state.auto_functions.items():
                if func_name in functions:
                    func_data = functions[func_name]
                    script_path = func_data.get('path')
                    break

        if script_path and func_data:
            # Capture the output
            captured_output = io.StringIO()
            with redirect_stdout(captured_output):
                try:
                    # Create a new namespace for the script
                    script_namespace = globals().copy()
                    
                    # Add all py_stealth functions to the namespace
                    for name, func in globals().items():
                        if callable(func) and not name.startswith('__'):
                            script_namespace[name] = func
                    
                    # Add all uo_globals functions to the namespace
                    import core.uo_globals
                    for name, func in vars(core.uo_globals).items():
                        if callable(func) and not name.startswith('__'):
                            script_namespace[name] = func

                    # Execute the script
                    with open(script_path, 'r') as script_file:
                        script_code = script_file.read()
                        exec(script_code, script_namespace)

                    if 'main' in script_namespace:
                        # Check if the main function expects an argument
                        import inspect
                        main_func = script_namespace['main']
                        if len(inspect.signature(main_func).parameters) > 0:
                            main_func(self)
                        else:
                            main_func()
                    else:
                        print(f"Error: 'main' function not found in {func_name}")
                except Exception as e:
                    print(f"Error executing {func_name}: {str(e)}")

            # Print the captured output
            print(captured_output.getvalue())
        else:
            print(f"Script file for {func_name} not found.")

    def update_auto_function_param(self, func_name, param_index, value):
        for category, functions in self.state.auto_functions.items():
            if func_name in functions:
                functions[func_name][f'variable{param_index + 1}'] = value
                break
        print(f"Updated parameter {param_index + 1} of {func_name} to {value}")

    def toggle_auto_function(self, func_name, enabled):
        for category, functions in self.state.auto_functions.items():
            if func_name in functions:
                functions[func_name]['enabled'] = enabled
                break
        print(f"{'Enabled' if enabled else 'Disabled'} auto function: {func_name}")

    def add_friend(self):
        self.friends_controller.add_friend()
        self.ui.friends_tab.populate_tree()

    def remove_friend(self, id):
        self.friends_controller.remove_friend(id)
        self.ui.friends_tab.populate_tree()

    def clear_friends(self):
        self.friends_controller.clear_friends()
        self.ui.friends_tab.populate_tree()

    def get_friends(self):
        return self.friends_controller.get_friends()

    def add_pet(self):
        print("MainController: add_pet called")  # Debug print
        self.pets_controller.add_pet()
        if self.ui:
            print("Updating UI pets tab")  # Debug print
            self.ui.pets_tab.populate_tree()
        else:
            print("UI not set, cannot update pets tab")  # Debug print

    def remove_pet(self, id):
        self.pets_controller.remove_pet(id)
        if self.ui:
            self.ui.pets_tab.populate_tree()

    def clear_pets(self):
        self.pets_controller.clear_pets()
        if self.ui:
            self.ui.pets_tab.populate_tree()

    def get_pets(self):
        return self.pets_controller.get_pets()

    def set_scripts_tab(self, scripts_tab):
        self.scripts_tab = scripts_tab

    def set_hotkeys_state(self, state):
        self.state.set_hotkeys_enabled(state)
        self.hotkeys_controller.set_all_hotkeys_state(state)
        print(f"Hotkeys {'enabled' if state else 'disabled'}")
        self.print_current_state()

    def set_loop_state(self, enabled):
        self.state.set_loop_enabled(enabled)
        print(f"Loop {'enabled' if enabled else 'disabled'}")
        self.print_current_state()

    def set_auto_functions_state(self, enabled):
        self.state.set_auto_functions_enabled(enabled)
        self.auto_functions_controller.set_all_auto_functions_state(enabled)
        print(f"Auto functions {'enabled' if enabled else 'disabled'}")
        self.print_current_state()
        if self.ui and hasattr(self.ui, 'auto_functions_tab'):
            self.ui.auto_functions_tab.update_auto_button_state(enabled)

    def print_current_state(self):
        print("\nCurrent Application State:")
        print(f"Hotkeys Enabled: {self.state.hotkeys_enabled}")
        print(f"Loop Enabled: {self.state.loop_enabled}")
        print(f"Auto Functions Enabled: {self.state.auto_functions_enabled}")
        print(f"Scripts Timeout: {self.state.scripts_timeout} ms")
        print(f"Auto Functions Timeout: {self.state.auto_functions_timeout} ms")
        print(f"Number of Hotkeys: {len(self.state.hotkeys)}")
        print(f"Number of Friends: {len(self.state.friends)}")
        print(f"Number of Pets: {len(self.state.pets)}")
        print(f"Number of Discovered Functions: {sum(len(funcs) for funcs in self.state.discovered_functions.values())}")
        print(f"Number of Auto Functions: {sum(len(funcs) for funcs in self.state.auto_functions.values())}")
        print()  # Empty line for better readability

    def get_discovered_functions(self):
        return self.state.discovered_functions

    def get_auto_functions(self):
        return self.state.auto_functions

    def run_script(self, func_name, loop, timeout):
        print(f"Running script: {func_name}")
        print(f"Loop: {'Enabled' if loop else 'Disabled'}")
        print(f"Timeout: {timeout} ms")

        # Find the script file path and function data
        script_path = None
        func_data = None
        for category, functions in self.state.discovered_functions.items():
            if func_name in functions:
                func_data = functions[func_name]
                script_path = func_data.get('path')
                break
        
        if script_path is None:
            for category, functions in self.state.auto_functions.items():
                if func_name in functions:
                    func_data = functions[func_name]
                    script_path = func_data.get('path')
                    break

        if script_path and func_data:
            # Capture the output
            captured_output = io.StringIO()
            with redirect_stdout(captured_output):
                try:
                    # Create a new namespace for the script
                    script_namespace = globals().copy()
                    
                    # Add all py_stealth functions to the namespace
                    for name, func in globals().items():
                        if callable(func) and not name.startswith('__'):
                            script_namespace[name] = func
                    
                    # Add all uo_globals functions to the namespace
                    import core.uo_globals
                    for name, func in vars(core.uo_globals).items():
                        if callable(func) and not name.startswith('__'):
                            script_namespace[name] = func

                    # Execute the script
                    with open(script_path, 'r') as script_file:
                        script_code = script_file.read()
                        exec(script_code, script_namespace)

                    if 'main' in script_namespace:
                        # Check if the main function expects an argument
                        import inspect
                        main_func = script_namespace['main']
                        if len(inspect.signature(main_func).parameters) > 0:
                            main_func(self)
                        else:
                            main_func()
                    else:
                        print(f"Error: 'main' function not found in {func_name}")
                except Exception as e:
                    print(f"Error executing {func_name}: {str(e)}")

            # Print the captured output
            print(captured_output.getvalue())
        else:
            print(f"Script file for {func_name} not found.")

    def run_script(self, func_name, loop, timeout):
        print(f"Running script: {func_name}")
        print(f"Loop: {'Enabled' if loop else 'Disabled'}")
        print(f"Timeout: {timeout} ms")

        # Find the script file path and function data
        script_path = None
        func_data = None
        for category, functions in self.state.discovered_functions.items():
            if func_name in functions:
                func_data = functions[func_name]
                script_path = func_data.get('path')
                break
        
        if script_path is None:
            for category, functions in self.state.auto_functions.items():
                if func_name in functions:
                    func_data = functions[func_name]
                    script_path = func_data.get('path')
                    break

        if script_path and func_data:
            # Capture the output
            captured_output = io.StringIO()
            with redirect_stdout(captured_output):
                try:
                    # Create a new namespace for the script
                    script_namespace = globals().copy()
                    
                    # Add all py_stealth functions to the namespace
                    for name, func in globals().items():
                        if callable(func) and not name.startswith('__'):
                            script_namespace[name] = func
                    
                    # Add all uo_globals functions to the namespace
                    import core.uo_globals
                    for name, func in vars(core.uo_globals).items():
                        if callable(func) and not name.startswith('__'):
                            script_namespace[name] = func

                    # Execute the script
                    with open(script_path, 'r') as script_file:
                        script_code = script_file.read()
                        exec(script_code, script_namespace)

                    if 'main' in script_namespace:
                        # Check if the main function expects an argument
                        import inspect
                        main_func = script_namespace['main']
                        if len(inspect.signature(main_func).parameters) > 0:
                            main_func(self)
                        else:
                            main_func()
                    else:
                        print(f"Error: 'main' function not found in {func_name}")
                except Exception as e:
                    print(f"Error executing {func_name}: {str(e)}")

            # Print the captured output
            print(captured_output.getvalue())
        else:
            print(f"Script file for {func_name} not found.")