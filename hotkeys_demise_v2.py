from py_stealth import *
import json
import tkinter as tk
from tkinter import ttk, messagebox
from pynput import keyboard
import inspect
from pynput.keyboard import Key, KeyCode
import time
from typing import Literal, get_args, TypeVar
from collections import defaultdict
import threading


def debug(message: str, color: Literal["success", "fail", "info", "warning"] = "info") -> None:
    color_map = {
        "success": 60,  # Green
        "fail": 30,     # Red
        "info": 10,      # Blue
        "warning": 40   # Orange
    }
    ClientPrintEx(Self(), color_map[color], 1, f"* {message.upper()} *")
    print(message)
    AddToSystemJournal(message)

def configurable_function(**kwargs):
    def decorator(func):
        func.config = kwargs
        return func
    return decorator

def exclude_from_gui(func):
    func._exclude_from_gui = True
    return func


# ------------------------------------------------------------------------------------

def main_loop():
    while True:
        if SystemFunctions.hotkeys_enabled:
            if Functions.autoheal_enabled:
                if GetHP(Self()) < MaxHP():
                    Functions.heal_self()
        time.sleep(0.1)  # Small delay to prevent excessive CPU usage



ConsumableType = Literal[
    "GREATER EXPLOSION", "GREATER STRENGTH", "GREATER HEAL", "GREATER REFRESHMENT",
    "GREATER AGILITY", "GREATER CURE", "GREATER CONFLAGRATION", "GREATER CONFUSION BLAST",
    "INVISIBILITY", "SMOKE BOMB", "ENCHANTED APPLE", "BOLAS", "ORANGE PETALS",
    "ROSE OF TRINSIC", "GRAPES OF WRATH", "RECALL"
]

class Functions:
    

    @exclude_from_gui
    def getTargetID() -> int :
        ClientRequestObjectTarget()
        WaitForClientTargetResponse(60000)
        if ClientTargetResponsePresent():
            response = ClientTargetResponse()
            if isinstance(response, dict):
                item_id = response.get('ID', None)
                return item_id
        return None

    @staticmethod
    @exclude_from_gui
    def consume(item: ConsumableType) -> bool:
        CONSUMABLE_MAP = {
            "GREATER EXPLOSION": (3853, 0),
            "GREATER STRENGTH": (3849, 0),
            "GREATER HEAL": (3852, 0),
            "GREATER REFRESHMENT": (3851, 0),
            "GREATER AGILITY": (3848, 0),
            "GREATER CURE": (3847, 0),
            "GREATER CONFLAGRATION": (3846, 1161),
            "GREATER CONFUSION BLAST": (3846, 1165),
            "INVISIBILITY": (3846, 306),
            "SMOKE BOMB": (10248, 0),
            "ENCHANTED APPLE": (12248, 1160),
            "BOLAS": (9900, 0),
            "ORANGE PETALS": (4129, 43),
            "ROSE OF TRINSIC": (4129, 14),
            "GRAPES OF WRATH": (12247, 1154),
            "RECALL": (8012, 0),
        }
        
        if item in CONSUMABLE_MAP:
            type, color = CONSUMABLE_MAP[item]
            if UseType(type, color):
                debug(f"Using {item}", "success")
                return True
            else:
                debug(f"MISSING {item}", "warning")
                return False
        else:
            debug(f"Unknown consumable: {item}", "warning")
            return False
        
    @staticmethod
    def singleGetInfo(id=None):
        if id is None:
            # debug("Please select a target...", "info")
            id = Functions.getTargetID()
            if id is None:
                debug("No target selected.", "info")
                return
        
        name = GetTooltip(id)
        info = f"Name: {name.split('|')[0]}, Type: {GetType(id)}, Color: {GetColor(id)}, ID: {id}"
        debug(info, "info")
        
    def containerGetInfo():
        id = Functions.getTargetID()
        if id != None:
            FindType(0xFFFF, id)
            if GetFindedList():
                print("----------")
                for item in GetFindedList():
                    Functions.singleGetInfo(item)
                print("----------")


    autoheal_enabled = False
    autoheal_threshold = 95  # Default value, can be changed via config
    
    @staticmethod
    def toggle_autoheal():
        Functions.autoheal_enabled = not Functions.autoheal_enabled
        debug(f"Autoheal {'enabled' if Functions.autoheal_enabled else 'disabled'}", 
              "success" if Functions.autoheal_enabled else "fail")


    @configurable_function(enabled=True, threshold=95)
    def heal_self():
        if Functions.consume("GREATER HEAL"):
            debug("Healing Self", "success")
            Wait(3000)
        else:
            debug("Healing not possible", "warning")

    @staticmethod
    def deconstruct_gump():
        for i in range(GetGumpsCount()):
            gump = GetGumpInfo(i)
            for entry in gump:
                debug(f"---------\n{entry}", "info")
                if len(entry) > 0:
                    subentries = gump[entry]
                    if isinstance(subentries, list):
                        for x in subentries:
                            debug(str(x), "info")
                    else:
                        debug(str(subentries), "info")

    def hide():
        if not Hidden():
            UseSkill('Hiding')
            debug("Not hidden", "warning")
        else:
            debug("Already hidden", "info")

    def cast_magic_arrow():
        debug("Casting Magic Arrow", "info")

    def cancel_target():
        if TargetPresent():
            CancelTarget()
            debug("Target Canceled", "warning")



    @exclude_from_gui
    def secret_function():
        # This function won't appear in the GUI
        pass

    def get_total_stats(show_resistances=True, show_bonuses=True, show_damage=True, 
                        show_hit_effects=True, show_durability=False, show_other=True, show_items=True):
        target = Functions.getTargetID()
        if target is None:
            debug("No target selected.", "warning")
            return

        name = GetName(target)
        debug("---------", "info")
        debug(f"Stats for: {name}", "info")

        items = [ObjAtLayerEx(layer, target) for layer in range(25) if ObjAtLayerEx(layer, target)]
        total_stats = defaultdict(float)

        for item in items:
            info = GetTooltip(item)
            for prop in info.split('|'):
                key, value = prop.rsplit(':', 1) if ':' in prop else prop.rsplit(' ', 1) if ' ' in prop else (None, None)
                if key and value:
                    try:
                        total_stats[key.strip().lower()] += float(value.strip().rstrip('%'))
                    except ValueError:
                        pass

        def normalize_stat_name(stat: str) -> str:
            stat = stat.lower().replace('total ', '')
            if 'durability' in stat:
                return 'durability'
            return stat

        def format_stat_value(stat: str, value: float) -> str:
            if 'resist' in stat or 'increase' in stat or 'reduction' in stat:
                return f"{value:.1f}%"
            if stat == 'durability':
                return f"{value:.0f}"
            if value == float('inf'):
                return "Infinite"
            if 'weapon damage' in stat:
                return f"{value:.0f}"
            return f"{value:.1f}"

        grouped_stats = defaultdict(dict)
        for stat, value in total_stats.items():
            normalized_stat = normalize_stat_name(stat)
            formatted_value = format_stat_value(normalized_stat, value)
            
            if 'resist' in normalized_stat:
                grouped_stats['Resistances'][normalized_stat] = formatted_value
            elif 'bonus' in normalized_stat or 'increase' in normalized_stat:
                grouped_stats['Bonuses'][normalized_stat] = formatted_value
            elif 'durability' in normalized_stat:
                grouped_stats['Durability'][stat] = formatted_value
            elif 'damage' in normalized_stat:
                if 'weapon damage' in normalized_stat:
                    parts = normalized_stat.split()
                    if len(parts) >= 3:
                        key = f"Weapon damage {parts[2]}"
                        grouped_stats['Damage'][key] = formatted_value
                else:
                    grouped_stats['Damage'][normalized_stat] = formatted_value
            elif 'hit' in normalized_stat:
                grouped_stats['Hit Effects'][normalized_stat] = formatted_value
            else:
                grouped_stats['Other'][normalized_stat] = formatted_value
        
        grouped_stats['Items'] = {f"Item {i+1}": GetTooltip(item).split('|')[0].strip() for i, item in enumerate(items)}
        
        sections_to_show = {
            'Resistances': show_resistances,
            'Bonuses': show_bonuses,
            'Damage': show_damage,
            'Hit Effects': show_hit_effects,
            'Durability': show_durability,
            'Other': show_other,
            'Items': show_items
        }

        order = ['Resistances', 'Bonuses', 'Damage', 'Hit Effects', 'Durability', 'Other', 'Items']
        for group in order:
            if group in grouped_stats and sections_to_show.get(group, True):
                debug(f"\n{group}:", "info")
                for stat, value in grouped_stats[group].items():
                    debug(f"  {stat.capitalize()}: {value}", "info")

        debug("---------", "info")







# ------------------------------------------------------------------------------------



class SystemFunctions:
    hotkeys_enabled = True

    @staticmethod
    def toggle_all_hotkeys():
        SystemFunctions.hotkeys_enabled = not SystemFunctions.hotkeys_enabled
        debug(f"Hotkeys {'enabled' if SystemFunctions.hotkeys_enabled else 'disabled'}", 
              "success" if SystemFunctions.hotkeys_enabled else "fail")

class HotkeyConfig:
    def __init__(self, master):
        self.master = master
        self.hotkey_listener = None
        try:
            self.update_title()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to Stealth: {str(e)}")
            self.master.title("Hotkey Configuration - Not Connected")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.hotkeys_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.hotkeys_frame, text="Hotkeys")

        self.tree = ttk.Treeview(self.hotkeys_frame, columns=('Function', 'Hotkey'), show='headings')
        self.tree.heading('Function', text='Function')
        self.tree.heading('Hotkey', text='Hotkey')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(self.hotkeys_frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Assign Hotkey", command=self.assign_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Hotkey", command=self.remove_hotkey).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save", command=self.save_config).pack(side=tk.LEFT, padx=5)

        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="Function Config")

        self.load_functions()
        self.load_config()

        self.hotkey_listener = None
        self.current_keys = set()
        self.last_activation_time = 0
        self.activation_cooldown = 0.3  # 300 milliseconds cooldown
        self.start_hotkey_listener()

    def update_title(self):
        try:
            char_name = GetName(Self())
            self.master.title(f"Hotkey Configuration - {char_name}")
        except Exception as e:
            raise Exception(f"Failed to get character name: {str(e)}")

    def load_functions(self):
        for func_name, func in inspect.getmembers(SystemFunctions, predicate=inspect.isfunction):
            if not func_name.startswith('__') and not getattr(func, '_exclude_from_gui', False):
                self.tree.insert('', 'end', values=(func_name, ''), tags=('system',))
        
        for func_name, func in inspect.getmembers(Functions, predicate=inspect.isfunction):
            if not func_name.startswith('__') and func_name != 'main_loop' and not getattr(func, '_exclude_from_gui', False):
                self.tree.insert('', 'end', values=(func_name, ''))
                if hasattr(func, 'config'):
                    self.create_function_config(func_name, func.config)

        self.tree.tag_configure('system', background='light gray')

    def create_function_config(self, func_name, config):
        frame = ttk.LabelFrame(self.config_frame, text=func_name)
        frame.pack(pady=5, padx=10, fill=tk.X)

        row_frame = ttk.Frame(frame)
        row_frame.pack(fill=tk.X, padx=5, pady=2)

        left_frame = ttk.Frame(row_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        right_frame = ttk.Frame(row_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.X)

        for param, default in config.items():
            if isinstance(default, bool):
                var = tk.BooleanVar(value=default)
                ttk.Checkbutton(left_frame, text=param, variable=var).pack(side=tk.LEFT)
            else:
                label_frame = ttk.Frame(right_frame)
                label_frame.pack(side=tk.RIGHT, padx=(10, 0))  # Add some padding to separate from the left side
                
                if isinstance(default, (int, float)):
                    var = tk.DoubleVar(value=default)
                    ttk.Entry(label_frame, textvariable=var, width=10).pack(side=tk.RIGHT)
                else:
                    var = tk.StringVar(value=str(default))
                    ttk.Entry(label_frame, textvariable=var, width=20).pack(side=tk.RIGHT)
                
                ttk.Label(label_frame, text=f"{param}:").pack(side=tk.RIGHT, padx=(0, 5))

            setattr(self, f"{func_name}_{param}", var)

    def load_config(self):
        try:
            with open('hotkey_config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}

        for func, data in self.config.items():
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == func:
                    hotkey = data.get('hotkey', '') if isinstance(data, dict) else data
                    self.tree.item(item, values=(func, hotkey))
                    if hasattr(Functions, func):
                        func_obj = getattr(Functions, func)
                        if hasattr(func_obj, 'config'):
                            for param, value in data.items() if isinstance(data, dict) else {}:
                                if param != 'hotkey':
                                    var = getattr(self, f"{func}_{param}", None)
                                    if var:
                                        var.set(value)
                    break

    def save_config(self):
        self.config = {}
        for item in self.tree.get_children():
            func, hotkey = self.tree.item(item)['values']
            if hotkey:
                self.config[func] = {"hotkey": hotkey}

        for func_name, func in inspect.getmembers(Functions, predicate=inspect.isfunction):
            if hasattr(func, 'config'):
                if func_name not in self.config:
                    self.config[func_name] = {}
                elif isinstance(self.config[func_name], str):
                    self.config[func_name] = {"hotkey": self.config[func_name]}
                for param in func.config:
                    var = getattr(self, f"{func_name}_{param}", None)
                    if var:
                        self.config[func_name][param] = var.get()

        with open('hotkey_config.json', 'w') as f:
            json.dump(self.config, f)
        messagebox.showinfo("Success", "Configuration saved successfully!")
        self.start_hotkey_listener()  # Restart the listener with new configuration
        self.update_title()  # Update the title in case the character name has changed

    def assign_hotkey(self, item=None):
        if item is None:
            selected = self.tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a function.")
                return
            item = selected[0]

        func = self.tree.item(item)['values'][0]
        self.master.title(f"Press hotkey for {func}")
        self.current_hotkey = []
        self.current_item = item
        self.master.bind('<KeyPress>', self.on_keypress)
        self.master.bind('<KeyRelease>', self.on_keyrelease)

    def on_keypress(self, event):
        key = self.get_key_string(event)
        if key not in self.current_hotkey:
            self.current_hotkey.append(key)
        # print(f"Key pressed: {key}")  # Debug: Print the pressed key

    def on_keyrelease(self, event):
        if len(self.current_hotkey) > 0:
            hotkey = '+'.join(self.current_hotkey)
            func = self.tree.item(self.current_item)['values'][0]
            self.tree.item(self.current_item, values=(func, hotkey))
            self.master.title("Hotkey Configuration")
            self.master.unbind('<KeyPress>')
            self.master.unbind('<KeyRelease>')

    def get_key_string(self, event):
        key = event.keysym.lower()
        if key in ['control_l', 'control_r']:
            return '<ctrl>'
        elif key in ['shift_l', 'shift_r']:
            return '<shift>'
        elif key in ['alt_l', 'alt_r']:
            return '<alt>'
        elif key == 'grave':
            return '<grave>'
        elif len(key) == 1:
            return f'<{key}>'  # Wrap single characters (including numbers) in angle brackets
        else:
            return f'<{key}>'

    def remove_hotkey(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a function.")
            return

        func = self.tree.item(selected[0])['values'][0]
        self.tree.item(selected[0], values=(func, ''))

    def on_double_click(self, event):
        item = self.tree.identify('item', event.x, event.y)
        if item:
            self.assign_hotkey(item)

    def start_hotkey_listener(self):
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        self.hotkey_listener = keyboard.Listener(on_press=self.on_key_press, on_release=self.on_key_release)
        self.hotkey_listener.start()

    def on_key_press(self, key):
        current_time = time.time()
        if current_time - self.last_activation_time < self.activation_cooldown:
            return  # Ignore rapid repeated activations

        if isinstance(key, keyboard.Key):
            self.current_keys.add(key)
        elif isinstance(key, keyboard.KeyCode):
            self.current_keys.add(key)
        
        self.check_hotkeys()

    def on_key_release(self, key):
        self.current_keys.discard(key)

    def check_hotkeys(self):
        for item in self.tree.get_children():
            func, hotkey_str = self.tree.item(item)['values']
            if hotkey_str:
                hotkey = self.parse_hotkey(hotkey_str)
                if all(k in self.current_keys for k in hotkey):
                    current_time = time.time()
                    if current_time - self.last_activation_time >= self.activation_cooldown:
                        self.activate_function(func)
                        self.last_activation_time = current_time
                    break  # Exit after first matching hotkey to prevent multiple activations

    def activate_function(self, func_name):
        if SystemFunctions.hotkeys_enabled or func_name == 'toggle_all_hotkeys':
            if hasattr(SystemFunctions, func_name):
                getattr(SystemFunctions, func_name)()
            elif hasattr(Functions, func_name):
                func = getattr(Functions, func_name)
                if callable(func):
                    func()
                else:
                    debug(f"Function {func_name} is not callable", "warning")
            else:
                debug(f"Function {func_name} not found", "warning")
        else:
            debug(f"Hotkey for {func_name} pressed, but hotkeys are disabled", "fail")

    def parse_hotkey(self, hotkey_str):
        keys = hotkey_str.lower().split('+')
        parsed = []
        for key in keys:
            if key == '<ctrl>':
                parsed.append(keyboard.Key.ctrl)
            elif key == '<alt>':
                parsed.append(keyboard.Key.alt)
            elif key == '<shift>':
                parsed.append(keyboard.Key.shift)
            elif key == '<grave>':
                parsed.append(keyboard.KeyCode.from_char('`'))
            elif key.startswith('<') and key.endswith('>'):
                parsed.append(keyboard.KeyCode.from_char(key[1:-1]))
            else:
                parsed.append(keyboard.KeyCode.from_char(key))
        return tuple(parsed)

    def __del__(self):
        if hasattr(self, 'hotkey_listener') and self.hotkey_listener:
            self.hotkey_listener.stop()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = HotkeyConfig(root)
        
        # Start the main loop in a separate thread
        main_thread = threading.Thread(target=main_loop, daemon=True)
        main_thread.start()

        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        # Clean up when the GUI is closed
        if hasattr(app, 'hotkey_listener') and app.hotkey_listener:
            app.hotkey_listener.stop()

    print("GUI closed. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")