from core.main_controller import MainController

def main(main_controller: MainController):
    new_state = main_controller.toggle_all_hotkeys()
    ClientPrintEx(Self(), 70 if new_state else 34, 3, f"* HOTKEYS {'ON' if new_state else 'OFF'} *")
    print(f"Hotkeys are now {'enabled' if new_state else 'disabled'}")

        # Update the UI if auto_functions_tab is available
    if main_controller.ui and hasattr(main_controller.ui, 'scripts_tab'):
        main_controller.ui.scripts_tab.update_auto_button_state(new_state)
    else:
        print("Warning: scripts_tab is not set, unable to update UI")