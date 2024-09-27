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
        self.ui = None

    def set_ui(self, ui):
        self.ui = ui

    def save_config(self):
        # Implement saving configuration
        pass

    def load_config(self):
        # Implement loading configuration
        pass

    # Add other methods as needed