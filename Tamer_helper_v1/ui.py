import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
import threading
from py_stealth import *
import json
import os
import sys
from datetime import datetime, timedelta

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ui_config import UI_CONFIG
from functions import *  # Import all functions from functions.py
from damage_counter import update_damage_counter, reset_damage_counter

class SimpleUI:
    def __init__(self, master):
        self.master = master
        master.title(UI_CONFIG["window_title"])
        master.configure(bg='black')

        self.script_name = os.path.basename(__file__).split('.')[0]
        self.char_name = CharName()
        self.config_file = f"{self.script_name}_{self.char_name}_config.json"

        # Initialize state with all button names from UI_CONFIG
        self.state = {key: False for key in UI_CONFIG["state_keys"]}
        for key in UI_CONFIG["list_keys"]:
            self.state[key] = []

        self.settings = UI_CONFIG["settings"].copy()

        self.buttons = {}
        self.create_bottom_frame()  # Create bottom frame first
        self.create_buttons()  # Then create buttons
        self.create_damage_counter()

        self.running = False
        self.start_time = None
        self.next_bandage_time = datetime.datetime.now()
        self.follow_target = None
        self.pets = []

        self.load_config()
        self.pets = self.state.get("PETS", [])  # Initialize pets from loaded state

        # Ensure all state keys from UI_CONFIG are present in self.state
        for key in UI_CONFIG["state_keys"]:
            if key not in self.state:
                self.state[key] = False

        # Print debug information
        print("Initialized state keys:", list(self.state.keys()))
        print("UI_CONFIG state_keys:", UI_CONFIG["state_keys"])

        # Add these lines at the end of __init__
        self.master.update_idletasks()
        self.master.geometry('')  # Reset geometry to allow auto-sizing
        self.master.resizable(False, False)  # Disable manual resizing

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
        row = 0
        col = 0
        visible_buttons = 0

        print("Debug: UI_CONFIG['buttons']:", UI_CONFIG["buttons"])

        for left, right in UI_CONFIG["buttons"]:
            for name in (left, right):
                if name and self.should_show_button(name):  # Check if name is not empty
                    print(f"Creating button: {name}")
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
                    
                    col += 1
                    visible_buttons += 1
                    if col == 2:
                        col = 0
                        row += 1
                else:
                    print(f"Skipping button: '{name}' (empty or should not show)")

        # Configure grid weights
        for i in range(row + 1):  # Ensure all rows are configured
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(2):  # Always 2 columns
            self.master.grid_columnconfigure(i, weight=1)

        # Update the bottom frame's row position
        if hasattr(self, 'bottom_frame'):
            self.bottom_frame.grid(row=row + 1, column=0, columnspan=2, sticky='nsew')
            self.master.grid_rowconfigure(row + 1, weight=0)

        print(f"Total visible buttons: {visible_buttons}")

        # Ensure the window size adjusts to the content
        self.master.update_idletasks()
        self.master.geometry('')

    def should_show_button(self, name):
        skill_requirements = {
            "HEAL": lambda: GetSkillValue("Magery") > 50 or GetSkillValue("Chivalry") > 50,
            "BANDAGE": lambda: GetSkillValue("Healing") > 50 or GetSkillValue("Veterinary") > 50,
            "DISCORD": lambda: GetSkillValue("Discordance") > 40 and GetSkillValue("Musicianship") > 40,
            "MORTAL": lambda: GetSkillValue("Chivalry") > 50,
            "PRI": lambda: GetSkillValue("Tactics") > 80,
            "SEC": lambda: GetSkillValue("Tactics") > 80,
            "EOO": lambda: GetSkillValue("Chivalry") > 50,
            "CW": lambda: GetSkillValue("Chivalry") > 50,
            "DF": lambda: GetSkillValue("Chivalry") > 50,
            "HONOR": lambda: GetSkillValue("Bushido") > 50,
            "LS": lambda: GetSkillValue("Bushido") > 50,
            "EB": lambda: GetSkillValue("Magery") > 50,
            "FS": lambda: GetSkillValue("Magery") > 50,
            "CURE": lambda: GetSkillValue("Magery") > 50,  # Add this line for CURE
        }

        if name in skill_requirements:
            return skill_requirements[name]()
        return True  # Show the button if there's no specific requirement

    def create_bottom_frame(self):
        self.bottom_frame = tk.Frame(self.master, bg='black')

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

    def create_damage_counter(self):
        damage_frame = tk.Frame(self.master, bg='black')
        damage_frame.grid(row=0, column=2, rowspan=len(UI_CONFIG["buttons"]), sticky='nsew')

        self.damage_text = tk.Text(damage_frame, width=UI_CONFIG["damage_counter"]["width"] // 2,
                                   height=UI_CONFIG["damage_counter"]["height"],
                                   bg='#333333', fg='white', font=('Courier', 12), padx=5, pady=5)
        self.damage_text.pack(fill=tk.BOTH, expand=True)
        self.damage_text.tag_configure('center', justify='center')

        self.damage_info = tk.Label(damage_frame, text="", bg='black', fg='white', font=('Courier', 10), justify=tk.LEFT)
        self.damage_info.pack(fill=tk.X, pady=(5, 0))

        self.update_damage_counter()  # Initial update

        # After creating the damage counter, configure its grid
        self.master.grid_columnconfigure(2, weight=0)

    def toggle_button(self, name):
        if not name:  # Check if name is empty
            print("Warning: Attempted to toggle a button with an empty name")
            return
        if name not in self.state:
            print(f"Warning: Button '{name}' not found in self.state")
            return
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
        if name in self.buttons:
            color = "#7FBC8F" if state else "#333333"
            text_color = 'black' if state else 'white'
            self.buttons[name].config(bg=color, fg=text_color)
        else:
            print(f"Warning: Button '{name}' not found in self.buttons")

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
        print("ClientRequestObjectTarget called")
        WaitForClientTargetResponse(60000)
        print("WaitForClientTargetResponse completed")
        if ClientTargetResponsePresent():
            new_id = ClientTargetResponse().get('ID')
            if new_id:
                new_name = GetName(new_id)
                new_item = (str(new_id), new_name)
                items = self.state[item_type.upper()]
                print(f"Current {item_type} list: {items}")
                
                # Check for duplicates based on ID
                if not any(item[0] == new_item[0] for item in items):
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


    def update_damage_counter(self):
        info = update_damage_counter()
        self.damage_text.delete('1.0', tk.END)
        
        # Display recent damages
        recent_damages = info.get('recent_damages', [])
        for damage in recent_damages:
            self.damage_text.insert(tk.END, f"{damage}\n", 'center')
        
        # Fill remaining lines if less than 10 recent damages
        for _ in range(10 - len(recent_damages)):
            self.damage_text.insert(tk.END, "[  ] [  ]\n", 'center')
        
        # Update the info label
        info_text = f"{info['status']}{info['name']}\n"
        info_text += f"Total: [{info['total_dmg_received']}] [{info['total_dmg_done']}]\n"
        info_text += f"DPS: {info['dps']:.2f} | DRPS: {info['drps']:.2f}\n"
        info_text += f"Time: {info['time']}"
        if not info.get('is_active', True):
            info_text += " (Final)"
        self.damage_info.config(text=info_text)
        
        # Schedule the next update
        self.master.after(1000, self.update_damage_counter)  # Update every second

    def main_loop(self):
        while True:
            settings = self.get_settings()
            
            if self.is_running():
                state = self.get_state()
                
                while Dead():
                    Wait(1000)
                
                # Follow
                if state[UI_CONFIG["follow_key"]] and settings["Follow Distance"] > 0 and state['follow_target']:
                    follow_id = int(state['follow_target'][0])
                    follow_distance = settings["Follow Distance"]
                    follow(follow_id, follow_distance)

                if state["EOO"]: EOO()
                if state["CW"]: CW()
                if state["DF"]: DF()
                if state['LS']: LS()
                if state['HONOR']: HONOR()
                if state['PRI']: PRI()
                if state['EB']: EB()
                if state['FS']: FS()
            
                # Heal friends and pets
                for list_key in ["PETS", "FRIENDS"]:
                    for id_str, name in state[list_key]:
                        try:
                            is_me = id_str == str(Self())
                            ID = int(id_str)
                            if IsObjectExists(ID) and GetDistance(ID) < 8:
                                is_friend = list_key == "FRIENDS"
                                is_pet = list_key == "PETS"
                                
                                # Mortal Strike logic
                                if state['MORTAL']:
                                    if is_friend and settings.get("Remove Mortal (Friends)", False):
                                        MORTAL(ID)
                                    if is_pet and settings.get("Remove Mortal (Pets)", False):
                                        MORTAL(ID)

                                # Cure logic
                                if state["CURE"]:
                                    remove_poison_friends = settings.get("Remove Poison (Friends)", False)
                                    remove_poison_pets = settings.get("Remove Poison (Pets)", False)
                                    if (is_friend and remove_poison_friends) or (is_pet and remove_poison_pets):
                                        threshold = settings.get("Friend Cure Threshold" if is_friend else "Pet Cure Threshold", 0)
                                        CURE(ID, threshold)
                                
                                # Heal logic
                                if state["HEAL"]:
                                    threshold = settings.get("Friend Heal Threshold" if is_friend else "Pet Heal Threshold", 0)
                                    hp = (GetHP(ID) / MaxHP()) * 100 if is_me else GetHP(ID) * 4
                                    if hp < threshold:
                                        Heal(ID, threshold)
                                        print(f"Healing {name} ({ID}) at {hp}% health, and {threshold} threshold")
                                
                                # Bandage logic
                                if state["BANDAGE"]:
                                    if is_friend and settings.get("Use Bandages (Friends)", False) and datetime.datetime.now() >= self.next_bandage_time:
                                        threshold = settings.get("Friend Bandage Threshold", 0)
                                        hp = (GetHP(ID) / MaxHP()) * 100 if is_me else GetHP(ID) * 4
                                        if hp < threshold:
                                            print(f"Applying bandage to {name} (HP: {hp:.1f}%, Threshold: {threshold}%)")
                                            BANDAGE(ID, threshold)
                                            try:
                                                buffs = GetBuffBarInfo()
                                                for buff in buffs:
                                                    if 'ClilocID1' in buff and GetClilocByID(buff['ClilocID1']).upper() == 'HEALING':
                                                        if 'TimeStart' in buff and 'Seconds' in buff:
                                                            buff_start_time = buff['TimeStart']
                                                            buff_duration = buff['Seconds']
                                                            buff_end_time = buff_start_time + timedelta(seconds=buff_duration)
                                                            self.next_bandage_time = buff_end_time + timedelta(seconds=1)
                                                            time_until_next = (self.next_bandage_time - datetime.datetime.now()).total_seconds()
                                                            print(f"Healing buff applied. Next bandage in {time_until_next:.1f} seconds")
                                                        else:
                                                            print(f"Warning: 'TimeStart' or 'Seconds' not found in healing buff: {buff}")
                                                        break
                                                else:
                                                    print("Warning: Healing buff not found after bandaging")
                                            except Exception as e:
                                                print(f"Error checking buffs: {str(e)}")
                                                print(f"Debug: Exception details: {type(e).__name__}, {e.args}")
                                    elif is_pet and settings.get("Use Veterinary", False):
                                        threshold = settings.get("Pet Bandage Threshold", 0)
                                        hp = (GetHP(ID) / MaxHP()) * 100 if is_me else GetHP(ID) * 4
                                        if hp < threshold:
                                            Veterinary(ID, threshold)
                        except ValueError:
                            print(f"Invalid ID for {name}: {id_str}")
                        except Exception as e:
                            print(f"Error processing {name} ({id_str}): {str(e)}")
                
                # Discord
                if state["DISCORD"]:
                    discord(state['FRIENDS'], state['PETS'])
                
            Wait(100)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleUI(root)
    
    # Start the main loop in a separate thread
    main_loop_thread = threading.Thread(target=app.main_loop)
    main_loop_thread.daemon = True
    main_loop_thread.start()
    
    # Center the window on the screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    root.mainloop()

    