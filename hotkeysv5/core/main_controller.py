from controllers.auto_discovery_controller import AutoDiscoveryController
from controllers.hotkeys_controller import HotkeysController
from controllers.friends_controller import FriendsController
from controllers.pets_controller import PetsController
from controllers.scripts_controller import ScriptsController
from controllers.auto_functions_controller import AutoFunctionsController
from core.state import State

class MainController:
    def __init__(self):
        self.state = State()
        self.hotkeys_controller = HotkeysController(self.state)
        self.friends_controller = FriendsController(self.state)
        self.pets_controller = PetsController(self.state)
        self.scripts_controller = ScriptsController(self.state)
        self.auto_functions_controller = AutoFunctionsController(self.state)
        self.auto_discovery_controller = AutoDiscoveryController(self.state)
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

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
        # This should be implemented in the ScriptsController
        self.scripts_controller.run_once(func_name)
        print(f"Running function once: {func_name}")
        self.print_current_state()

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
        new_state = self.auto_functions_controller.toggle_all_auto_functions()
        self.state.set_auto_functions_enabled(new_state)
        print(f"Auto functions {'enabled' if new_state else 'disabled'}")
        self.print_current_state()
        return new_state

    def toggle_all_hotkeys(self):
        new_state = self.hotkeys_controller.toggle_all_hotkeys()
        self.state.set_hotkeys_enabled(new_state)
        print(f"Hotkeys {'enabled' if new_state else 'disabled'}")
        self.print_current_state()
        return new_state

    def save_config(self):
        # Implement saving configuration
        pass

    def load_config(self):
        # Implement loading configuration
        pass

    def discover_all_functions(self):
        self.auto_discovery_controller.discover_all_functions()

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
        print(f"Number of Scripts: {len(self.state.scripts)}")
        print(f"Number of Auto Functions: {len(self.state.auto_functions)}")
        print()  # Empty line for better readability
