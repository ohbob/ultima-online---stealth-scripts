from core.main_controller import MainController

def main(main_controller: MainController):
    new_state = main_controller.toggle_all_hotkeys()
    print(f"Hotkeys are now {'enabled' if new_state else 'disabled'}")
    
    # Update the UI if scripts_tab is available
    if main_controller.scripts_tab:
        main_controller.scripts_tab.update_hotkey_button_state(new_state)
    else:
        print("Warning: scripts_tab is not set, unable to update UI")