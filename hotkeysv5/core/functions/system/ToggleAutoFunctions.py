from core.main_controller import MainController

def main(main_controller: MainController):
    new_state = main_controller.toggle_all_auto_functions()
    print(f"Auto functions are now {'enabled' if new_state else 'disabled'}")
    ClientPrintEx(Self(), 70 if new_state else 34, 3, f"* A-FUN {'ON' if new_state else 'OFF'} *")

    # Update the UI if auto_functions_tab is available
    if main_controller.ui and hasattr(main_controller.ui, 'auto_functions_tab'):
        main_controller.ui.auto_functions_tab.update_auto_button_state(new_state)
    else:
        print("Warning: auto_functions_tab is not set, unable to update UI")