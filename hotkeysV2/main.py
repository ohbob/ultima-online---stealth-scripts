import tkinter as tk
from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import time
import threading
from hotkey_config import load_config, parse_hotkey, HotkeyConfig
from utils import SystemFunctions
import game_functions

def on_activate(func_name, func_config):
    if SystemFunctions.hotkeys_enabled or func_name == 'toggle_all_hotkeys':
        if hasattr(SystemFunctions, func_name):
            getattr(SystemFunctions, func_name)()
        elif hasattr(game_functions, func_name):
            func = getattr(game_functions, func_name)
            if func_name == 'toggle_autoheal':
                game_functions.toggle_autoheal()
            else:
                if func_config:
                    for key, value in func_config.items():
                        setattr(game_functions, f"{func_name}_{key}", value)
                if 'enabled' in func_config:
                    current_state = getattr(game_functions, f"{func_name}_enabled", True)
                    setattr(game_functions, f"{func_name}_enabled", not current_state)
                func()
    else:
        print(f"Hotkey for {func_name} pressed, but hotkeys are disabled")

def start_hotkey_listener():
    config = load_config()

    hotkeys = {}
    for func, data in config.items():
        if isinstance(data, dict):
            hotkey_str = data['hotkey']
            func_config = {k: v for k, v in data.items() if k != 'hotkey'}
        else:
            hotkey_str = data
            func_config = {}
        
        hotkey = parse_hotkey(hotkey_str)
        hotkeys[hotkey] = (func, func_config)

    print("Registered hotkeys:", ['+'.join(str(k) for k in combo) for combo in hotkeys.keys()])

    current_keys = set()

    def on_press(key):
        if isinstance(key, Key):
            current_keys.add(key)
        elif isinstance(key, KeyCode):
            current_keys.add(key)
        
        # Check for custom hotkeys
        for hotkey, (func, func_config) in hotkeys.items():
            if all(k in current_keys for k in hotkey):
                on_activate(func, func_config)
                return

    def on_release(key):
        current_keys.discard(key)

    main_thread = threading.Thread(target=game_functions.main_loop, daemon=True)
    main_thread.start()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print("Hotkeys activated. Press keys to test. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        listener.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotkeyConfig(root)
    
    # Start the hotkey listener in a separate thread
    hotkey_thread = threading.Thread(target=start_hotkey_listener, daemon=True)
    hotkey_thread.start()
    
    # Run the GUI main loop
    root.mainloop()