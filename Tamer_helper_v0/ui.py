import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
import threading
from py_stealth import *
import json
import os
import sys

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui_config import UI_CONFIG

class SimpleUI:
    def __init__(self, master):
        self.master = master
        master.geometry(UI_CONFIG["window_size"])
        master.title(UI_CONFIG["window_title"])
        master.configure(bg='black')

        self.script_name = os.path.basename(__file__).split('.')[0]
        self.char_name = CharName()
        self.config_file = f"{self.script_name}_{self.char_name}_config.json"

        self.state = {key: False for key in UI_CONFIG["state_keys"]}
        for key in UI_CONFIG["list_keys"]:
            self.state[key] = []

        self.settings = UI_CONFIG["settings"].copy()

        self.buttons = {}
        self.create_buttons()
        self.create_bottom_frame()

        self.running = False
        self.start_time = None

        self.follow_target = None
        self.pets = []

        self.load_config()
        self.pets = self.state.get("PETS", [])  # Initialize pets from loaded state

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.state = config.get("state", self.state)
                loaded_settings = config.get("settings", {})
                
                # Update settings with loaded values, keeping defaults for missing keys
                for key, value in loaded_settings.items():
                    if key in self.settings:
                        self.settings[key] = value
                
                self.pets = self.state.get("PETS", [])  # Load pets from state
                
                # Update button states based on loaded configuration
                for button_name in self.buttons:
                    if button_name in self.state:
                        self.update_button_state(button_name, self.state[button_name])
        except FileNotFoundError:
            print("Config file not found. Using default settings.")
        except json.JSONDecodeError:
            print("Error reading config file. Using default settings.")

    def save_config(self):
        self.state["PETS"] = self.pets  # Ensure pets are in the state before saving
        config = {
            "state": self.state,
            "settings": self.settings
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Configuration saved to {self.config_file}")

    def create_buttons(self):
        for row, (left, right) in enumerate(UI_CONFIG["buttons"]):
            for col, name in enumerate((left, right)):
                button = tk.Button(self.master, text=name, width=8, height=1,
                                   command=lambda n=name: self.toggle_button(n),
                                   bg='#333333', fg='white',
                                   activebackground='#7FBC8F',
                                   activeforeground='black',
                                   bd=1, relief=tk.RAISED,
                                   highlightbackground='black',
                                   highlightthickness=1)
                button.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
                self.buttons[name] = button

        for i in range(3):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.master.grid_columnconfigure(i, weight=1)

    def create_bottom_frame(self):
        self.bottom_frame = tk.Frame(self.master, bg='black')
        self.bottom_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')

        self.timer_label = tk.Label(self.bottom_frame, text="00:00:00", 
                                    bg='black', fg='white', font=('Arial', 10))
        self.timer_label.pack(side=tk.TOP, fill=tk.X, pady=(5,0))

        button_frame = tk.Frame(self.bottom_frame, bg='black')
        button_frame.pack(side=tk.TOP, fill=tk.X)

        self.start_stop_button = tk.Button(button_frame, text="▶", width=5, height=1,
                                           command=self.toggle_start_stop,
                                           bg='#e7bb64', fg='black',
                                           activebackground='#8f8e95',
                                           activeforeground='white',
                                           bd=1, relief=tk.RAISED,
                                           highlightbackground='black',
                                           highlightthickness=1)
        self.start_stop_button.pack(side=tk.LEFT, fill=tk.X, padx=(5,2), pady=5)

        self.settings_button = tk.Button(button_frame, text="⚙", width=5, height=1,
                                         command=self.open_settings,
                                         bg='#333333', fg='white',
                                         activebackground='#7FBC8F',
                                         activeforeground='black',
                                         bd=1, relief=tk.RAISED,
                                         highlightbackground='black',
                                         highlightthickness=1)
        self.settings_button.pack(side=tk.LEFT, fill=tk.X, padx=(2,5), pady=5)

    def toggle_button(self, name):
        self.state[name] = not self.state[name]
        self.update_button_state(name, self.state[name])
        print(f"Debug: {name} toggled to {self.state[name]}")
        
        if name == UI_CONFIG["follow_key"]:
            if self.state[name]:
                self.request_follow_target()
            else:
                self.clear_follow_target()
        
        self.save_config()  # Save the updated state

    def update_button_state(self, name, state):
        color = "#7FBC8F" if state else "#333333"
        text_color = 'black' if state else 'white'
        self.buttons[name].config(bg=color, fg=text_color)

    def toggle_start_stop(self):
        self.running = not self.running
        if self.running:
            self.start_stop_button.config(text="■", bg='#8f8e95')
            self.start_time = time.time()
            self.update_timer()
        else:
            self.start_stop_button.config(text="▶", bg='#e7bb64')
            self.timer_label.config(text="00:00:00")

    def update_timer(self):
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.config(text=time_str)
            self.master.after(1000, self.update_timer)

    def open_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title(UI_CONFIG["settings_window"]["title"])
        settings_window.geometry(UI_CONFIG["settings_window"]["size"])
        settings_window.configure(bg='black')

        main_frame = tk.Frame(settings_window, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        frames = {}
        for section, title in UI_CONFIG["settings_window"]["sections"].items():
            frames[section] = tk.LabelFrame(main_frame, text=title, bg='black', fg='white', padx=10, pady=10)
            frames[section].grid(row=1 if section != 'shared' else 0, 
                                 column=0 if section != 'pets' else 1, 
                                 columnspan=2 if section == 'shared' else 1, 
                                 padx=10, pady=10, sticky='nsew')

        for setting in UI_CONFIG["numeric_settings"]:
            frame = frames['shared'] if setting in UI_CONFIG["shared_settings"] else \
                    frames['friends'] if setting in UI_CONFIG["friend_settings"] else frames['pets']
            self.create_numeric_setting(frame, setting)

        for setting in UI_CONFIG["boolean_settings"]:
            frame = frames['friends'] if setting in UI_CONFIG["friend_settings"] else frames['pets']
            self.create_checkbox(frame, setting)

        for dropdown in UI_CONFIG["settings_window"]["dropdown_settings"]:
            frame = tk.Frame(frames['shared'], bg='black')
            frame.pack(fill=tk.X, pady=5)
            tk.Label(frame, text=f"{dropdown['name']}:", bg='black', fg='white').pack(side=tk.LEFT)
            var = tk.StringVar(value=self.settings.get(dropdown['name'], dropdown['options'][0]))
            menu = tk.OptionMenu(frame, var, *dropdown['options'])
            menu.config(bg='#333333', fg='white', activebackground='#555555', activeforeground='white')
            menu.pack(side=tk.RIGHT)
            setattr(self, f"{dropdown['name'].replace(' ', '_').lower()}_var", var)

        for section in UI_CONFIG["list_sections"]:
            self.create_list_section(frames[section.lower()], section, 
                                     self.state["FRIENDS"] if section == "Friends" else self.pets)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        save_button = tk.Button(settings_window, text="Save", command=self.save_settings,
                                bg='#333333', fg='white', activebackground='#555555', activeforeground='white')
        save_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def create_numeric_setting(self, parent, key):
        frame = tk.Frame(parent, bg='black')
        frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(frame, text=f"{key}:", bg='black', fg='white')
        label.pack(side=tk.LEFT)
        
        var = tk.IntVar(value=self.settings.get(key, 0))
        widget = tk.Entry(frame, textvariable=var, width=10, bg='#333333', fg='white', insertbackground='white')
        widget.pack(side=tk.RIGHT)
        setattr(self, f"{key.replace(' ', '_').lower()}_var", var)

    def create_checkbox(self, parent, text):
        var = tk.BooleanVar(value=self.settings.get(text, False))
        checkbox = tk.Checkbutton(parent, text=text, variable=var,
                                  bg='black', fg='white', selectcolor='black',
                                  activebackground='black', activeforeground='white')
        checkbox.pack(anchor='w', pady=2)
        setattr(self, f"{text.replace(' ', '_').lower()}_var", var)

    def create_list_section(self, parent, title, items):
        frame = tk.Frame(parent, bg='black')
        frame.pack(fill=tk.BOTH, expand=True, pady=5)

        listbox = tk.Listbox(frame, bg='#333333', fg='white', selectbackground='#555555')
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)

        for item in items:
            listbox.insert(tk.END, f"{item[1]} ({item[0]})")

        button_frame = tk.Frame(parent, bg='black')
        button_frame.pack(fill=tk.X)

        add_button = tk.Button(button_frame, text="+", width=2,
                               command=lambda: self.add_item(title, listbox),
                               bg='#333333', fg='white', activebackground='#555555', activeforeground='white')
        add_button.pack(side=tk.LEFT, padx=2, pady=2)

        remove_button = tk.Button(button_frame, text="-", width=2,
                                 command=lambda: self.remove_item(title, listbox),
                                 bg='#333333', fg='white', activebackground='#555555', activeforeground='white')
        remove_button.pack(side=tk.LEFT, padx=2, pady=2)

        setattr(self, f"{title.lower()}_listbox", listbox)

    def add_item(self, item_type, listbox):
        self.master.after(0, lambda: self._add_item_thread(item_type, listbox))

    def _add_item_thread(self, item_type, listbox):
        print(f"Please select a {item_type[:-1]} to add in the game.")
        ClientRequestObjectTarget()
        WaitForClientTargetResponse(60000)
        if ClientTargetResponsePresent():
            new_id = ClientTargetResponse().get('ID')
            if new_id:
                new_name = GetName(new_id)
                new_item = (str(new_id), new_name)
                items = self.state[item_type.upper()]
                if new_item not in items:
                    items.append(new_item)
                    listbox.insert(tk.END, f"{new_name} ({new_id})")
                    print(f"Added new {item_type[:-1]}: {new_item}")
                    self.state[item_type.upper()] = items
                    self.save_config()
                else:
                    print(f"{new_name} is already in the {item_type} list.")
            else:
                print("Failed to get target ID.")
        else:
            print("No target selected.")

    def remove_item(self, item_type, listbox):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            item_str = listbox.get(index)
            item_id = item_str.split('(')[-1].split(')')[0]
            items = self.state[item_type.upper()]
            for item in items:
                if item[0] == item_id:
                    items.remove(item)
                    break
            listbox.delete(index)
            print(f"Removed {item_type[:-1]}: {item_str}")
            self.state[item_type.upper()] = items
            self.save_config()

    def save_settings(self):
        for key in UI_CONFIG["settings"].keys():
            var_name = f"{key.replace(' ', '_').lower()}_var"
            if hasattr(self, var_name):
                var = getattr(self, var_name)
                if isinstance(var, tk.BooleanVar):
                    self.settings[key] = var.get()
                elif isinstance(var, tk.IntVar):
                    try:
                        self.settings[key] = int(var.get())
                    except ValueError:
                        print(f"Invalid value for {key}. Using previous value.")
                elif isinstance(var, tk.StringVar):
                    self.settings[key] = var.get()

        print("Settings saved:", self.settings)
        self.save_config()

    def request_follow_target(self):
        self.master.after(0, self._request_follow_target_thread)

    def _request_follow_target_thread(self):
        print("Please select a target to follow in the game.")
        ClientRequestObjectTarget()
        WaitForClientTargetResponse(60000)
        if ClientTargetResponsePresent():
            new_id = ClientTargetResponse().get('ID')
            if new_id:
                new_name = GetName(new_id)
                self.follow_target = (str(new_id), new_name)
                print(f"Now following: {new_name} (ID: {new_id})")
            else:
                print("Failed to get target ID.")
                self.clear_follow_target()
        else:
            print("No target selected.")
            self.clear_follow_target()

    def clear_follow_target(self):
        self.follow_target = None
        print("Follow target cleared.")

    def get_state(self):
        state = self.state.copy()
        state['follow_target'] = self.follow_target
        return state

    def get_settings(self):
        return self.settings.copy()

    def is_running(self):
        return self.running

from functions import *

def main_loop(app):
    while True:
        settings = app.get_settings()
        
        if app.is_running():
            state = app.get_state()
            
            while Dead():
                Wait(1000)
            
            # Follow
            if state[UI_CONFIG["follow_key"]] and settings["Follow Distance"] > 0 and state['follow_target']:
                follow_id = int(state['follow_target'][0])
                follow_distance = settings["Follow Distance"]
                follow(follow_id, follow_distance)

            # Heal friends and pets
            for list_key in ["PETS", "FRIENDS"]:
                for id_str, name in state[list_key]:
                    try:
                        is_me = id_str == str(Self())
                        ID = int(id_str)
                        if IsObjectExists(ID) and GetDistance(ID) < 8:
                            is_friend = list_key == "FRIENDS"
                            is_pet = list_key == "PETS"
                            
                            # Heal logic
                            if state["HEAL"]:
                                # Mortal Strike logic
                                if state['MORTAL']:
                                    if is_friend and settings.get("Remove Mortal (Friends)", False):
                                        RemoveMortal(ID)
                                    if is_pet and settings.get("Remove Mortal (Pets)", False):
                                        RemoveMortal(ID)
                                # Cure logic
                                if state["CURE"]:
                                    remove_poison_friends = settings.get("Remove Poison (Friends)", False)
                                    remove_poison_pets = settings.get("Remove Poison (Pets)", False)
                                    if (is_friend and remove_poison_friends) or (is_pet and remove_poison_pets):
                                        threshold = settings.get("Friend Cure Threshold" if is_friend else "Pet Cure Threshold", 0)
                                        Cure(ID, threshold)
                                        # print(f"Curing {'friend' if is_friend else 'pet'} {name} ({ID}) at {threshold}% poison")
                                # Heal logic
                                threshold = settings.get("Friend Heal Threshold" if is_friend else "Pet Heal Threshold", 0)
                                # hp = GetHP(ID) if not is_me else GetHP(ID) * 4

                                if is_me:
                                    hp = (GetHP(ID) / MaxHP()) * 100
                                else:
                                    hp = GetHP(ID) * 4
                                # print("-----------------------")
                                # print(f"Healing {name} ({ID}) at {hp}% health")
                                # print("Your real hp", GetHP(Self()))
                                # print("-----------------------")
                                if hp < threshold:
                                    Heal(ID, threshold)
                                    # print(f"Healing {name} ({ID}) at {hp}% health")
                            
                            # Bandage logic
                            if state["BANDAGE"]:
                                if is_friend and settings.get("Use Bandages (Friends)", False):
                                    threshold = settings.get("Friend Bandage Threshold", 0)
                                    if is_me:
                                        hp = (GetHP(ID) / MaxHP()) * 100
                                    else:
                                        hp = GetHP(ID) * 4
                                    if hp < threshold:
                                        Bandage(ID, threshold)
                                        # print(f"Bandaging friend {name} ({ID}) at {threshold}% health")
                                elif is_pet and settings.get("Use Veterinary", False):
                                    threshold = settings.get("Pet Bandage Threshold", 0)
                                    if is_me:
                                        hp = (GetHP(ID) / MaxHP()) * 100
                                    else:
                                        hp = GetHP(ID) * 4
                                    if hp < threshold:
                                        Veterinary(ID, threshold)
                                        # print(f"Using Veterinary on pet {name} ({ID}) at {threshold}% health")
                    except ValueError:
                        print(f"Invalid ID for {name}: {id_str}")
                    except Exception as e:
                        print(f"Error processing {name} ({id_str}): {str(e)}")
            
            # Discord
            if state["DISCORD"]:
                discord(state['FRIENDS'], state['PETS'])
                # print("Using Discord")
                # Implement Discord logic here
            
            # # Print friends and pets lists (consider doing this less frequently to reduce spam)
            # for list_key in UI_CONFIG["list_keys"]:
            #     items_str = ', '.join([f"{name} ({id})" for id, name in state[list_key]])
            #     print(f"{list_key}: {items_str}")
        
        # time.sleep(settings.get("Scan Frequency (ms)", 1000) / 1000)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleUI(root)
    
    # Start the main loop in a separate thread
    main_loop_thread = threading.Thread(target=main_loop, args=(app,))
    main_loop_thread.daemon = True
    main_loop_thread.start()
    
    root.mainloop()

    