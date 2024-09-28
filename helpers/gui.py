import tkinter as tk
import threading
import time
import configparser
import os
import sys
from tkinter import ttk, Entry, Listbox, Scrollbar

# Define global variables
toggle_states = {}
toggle_button = None
started = False
label_to_variable = {}
root = None
status = ""
status_label = None
timer_label = None
start_time = None
variable_labels = {}
entry_widgets = {}
list_widgets = {}

# Load configuration from file
config = configparser.ConfigParser()
config_filename = f'config_{os.path.splitext(os.path.basename(sys.argv[0]))[0]}.ini'
config.read(config_filename)

# Add this near the other global variables
autosave_timer = None

def autosave_config():
    global autosave_timer
    root.after(0, save_config)  # Schedule save_config to run in the main thread
    # print("Configuration autosaved.")
    # Schedule the next autosave in 60 seconds
    autosave_timer = threading.Timer(60, autosave_config)
    autosave_timer.start()

def update_variable_value(var_name, new_value):
    setval(var_name, new_value)

def getval(var_name):
    if var_name == 'started':
        return started
    elif var_name.startswith('toggle_'):
        toggle_name = var_name[7:]  # Remove 'toggle_' prefix
        if toggle_name in toggle_states:
            return toggle_states[toggle_name].get()
        else:
            print(f"Warning: Toggle '{toggle_name}' not found.")
            return False
    elif var_name in variable_labels:
        return variable_labels[var_name]['text'].split(': ')[1]
    else:
        print(f"Warning: Variable '{var_name}' not found in GUI.")
        return None

def setval(var_name, new_value):
    if var_name in variable_labels:
        variable_labels[var_name].config(text=f"{var_name}: {new_value}")
        autosave_config()  # Trigger autosave when a value is set
    else:
        print(f"Warning: Variable '{var_name}' not found in GUI.")

def create_gui(elements):
    global toggle_states, label_to_variable, root, status_label, timer_label, variable_labels, entry_widgets, list_widgets

    root = tk.Tk()
    root.title("Camo gui builder")
    root.geometry("300x840")  # Increased width from 250 to 300

    create_start_stop_row()  # Create Start/Stop button row

    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    toggle_frame = tk.Frame(main_frame)
    toggle_count = 0
    button_frame = None
    button_count = 0

    for element in elements:
        if element[0] == "button":
            _, button_text, button_callback, bg, active_bg = element
            if button_count % 2 == 0:
                button_frame = tk.Frame(main_frame)
                button_frame.pack(side=tk.TOP, fill=tk.X)

            button = tk.Button(button_frame, text=button_text, command=button_callback, 
                               bg=bg, activebackground=active_bg, 
                               activeforeground="white", padx=8, pady=5)
            button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
            button_count += 1

        elif element[0] == "variable":
            _, var_name, var_value = element
            saved_value = config.get('Variables', var_name, fallback=var_value)
            variable_frame = tk.Frame(main_frame)
            variable_frame.pack(side=tk.TOP, fill=tk.X)
            label = tk.Label(variable_frame, text=f"{var_name}: {saved_value}", anchor="w", padx=4, pady=2)
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            variable_labels[var_name] = label

        elif element[0] == "separator":
            _, orientation = element
            separator = ttk.Separator(main_frame, orient=orientation)
            separator.pack(fill=tk.X if orientation == 'horizontal' else tk.Y, pady=5)

        elif element[0] == "entry":
            _, name, default_value = element
            saved_value = config.get('Entries', name, fallback=default_value)
            entry_frame = tk.Frame(main_frame)
            entry_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)  # Add padding
            
            # Label takes 2/3 of the width
            label = tk.Label(entry_frame, text=f"{name}:", anchor="w", padx=4, pady=2)
            label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
            
            # Entry takes 1/3 of the width
            entry = Entry(entry_frame, width=10)  # Set a fixed width
            entry.insert(0, saved_value)
            entry.pack(side=tk.RIGHT, padx=(0, 5))  # Add right padding
            
            entry_widgets[name] = entry

            # Configure the frame to give more space to the label
            entry_frame.grid_columnconfigure(0, weight=2)  # Label column
            entry_frame.grid_columnconfigure(1, weight=1)  # Entry column

        elif element[0] == "list":
            _, name, items, height, command = element
            saved_items = config.get('Lists', name, fallback=None)
            if saved_items:
                items = eval(saved_items)  # Convert string representation back to list
            list_frame = tk.Frame(main_frame)
            list_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)  # Add padding
            label = tk.Label(list_frame, text=f"{name}:", anchor="w", padx=4, pady=2)
            label.pack(side=tk.TOP, fill=tk.X)
            scrollbar = Scrollbar(list_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox = Listbox(list_frame, yscrollcommand=scrollbar.set, height=height)
            for item in items:
                listbox.insert(tk.END, item)
            listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
            scrollbar.config(command=listbox.yview)
            list_widgets[name] = listbox
            if command:
                listbox.bind('<<ListboxSelect>>', command)

    # TIMER ---------------------
    timer_label = tk.Label(root, text="", anchor="w", padx=8, pady=5)
    timer_label.pack(side=tk.TOP, fill=tk.X)
    # END TIMER -----------------

    # STATUS --------------------
    status_label = tk.Label(root, text="Status: ", anchor="w", padx=8, pady=5)
    status_label.pack(side=tk.TOP, fill=tk.X)
    # END STATUS ----------------

    update_status()  # Start status update loop

def create_start_stop_row():
    global toggle_button
    toggle_button = tk.Button(root, text="Start", bg="#e7bb64", command=toggle_global)
    toggle_button.pack(side=tk.BOTTOM, fill=tk.X)  # Button at the bottom, takes the whole width

def toggle_global():
    global started, start_time, status
    started = not started
    toggle_button.config(text="Stop" if started else "Start", bg="#8f8e95" if started else "#e7bb64")
    save_config()
    status = "Running" if started else "Stopped"  # Update status variable
    if started:
        start_time = time.time()
        update_timer()

def toggle_function(func_name):
    current_state = g.getval(f"toggle_{func_name}")
    new_state = not current_state
    g.setval(f"toggle_{func_name}", new_state)
    
    if new_state:
        g.set_button_color(func_name, '#4CAF50')  # Green when toggled on
    else:
        g.set_button_color(func_name, '#F0F0F0')  # Light gray when toggled off
    
    print(f"Debug: {func_name} toggled to {new_state}")

def save_config():
    config['Toggles'] = {variable: str(toggle_states[label].get()) for label, variable in label_to_variable.items()}
    config['Variables'] = {var_name: variable_labels[var_name]['text'].split(': ')[1] for var_name in variable_labels}
    config['Entries'] = {name: entry.get() for name, entry in entry_widgets.items()}
    config['Lists'] = {name: list(listbox.get(0, tk.END)) for name, listbox in list_widgets.items()}
    with open(config_filename, 'w') as configfile:
        config.write(configfile)

def update_status():
    global status
    status_text = f"Status: {status}"
    status_label.config(text=status_text)
    root.after(1000, update_status)

def update_timer():
    global start_time
    if started:
        elapsed_time = time.time() - start_time
        timer_text = format_time(elapsed_time)
        timer_label.config(text=timer_text)
        root.after(1000, update_timer)

def format_time(seconds):
    intervals = [
        ('weeks', 604800),
        ('days', 86400),
        ('hours', 3600),
        ('minutes', 60),
        ('seconds', 1)
    ]
    result = []
    for name, count in intervals:
        value = int(seconds) // count
        if value > 0:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append(f"{value} {name}")
    return ', '.join(result)

def start_toggles_loop(callback):
    if callback is not None:
        toggle_thread = threading.Thread(target=callback, daemon=True)
        toggle_thread.start()

def run_gui():
    autosave_config()  # Start the autosave timer
    root.mainloop()
    if autosave_timer:
        autosave_timer.cancel()  # Stop the autosave timer when the GUI is closed

# Add this at the top of the file, after the imports
class GUIWrapper:
    def __init__(self):
        self.elements = []  # List to store all elements in order
        self.toggle_functions = {}
        self.root = None  # Add this line

    def add(self, element_type, *args, **kwargs):
        if element_type == "toggle":
            label, function = args
            self.elements.append(("toggle", label, function))
            self.toggle_functions[label] = function
        elif element_type == "variable":
            name, value = args
            self.elements.append(("variable", name, value))
        elif element_type == "button":
            label, function = args
            bg = kwargs.get('bg', '#F0F0F0')  # Default background color
            active_bg = kwargs.get('active_bg', '#4CAF50')  # Default active background color
            self.elements.append(("button", label, function, bg, active_bg))
        elif element_type == "separator":
            self.elements.append(("separator", args[0]))
        elif element_type == "entry":
            name, default_value = args
            self.elements.append(("entry", name, default_value))
        elif element_type == "list":
            name, items = args
            height = kwargs.get('height', 5)  # Default height is 5
            command = kwargs.get('command', None)
            self.elements.append(("list", name, items, height, command))

    def create_gui(self):
        global root
        create_gui(self.elements)
        self.root = root  # Store the root window
        for element in self.elements:
            if element[0] == "toggle":
                toggle_function(element[1])

    def start_toggles_loop(self, callback):
        start_toggles_loop(callback)

    def run_gui(self):
        run_gui()

    def get_active_toggles(self):
        return [self.toggle_functions[label] for label in self.toggle_functions if toggle_states.get(label, False)]

    def setval(self, var_name, new_value):
        root.after(0, lambda: setval(var_name, new_value))

    def getval(self, var_name):
        return getval(var_name)

    def get_entry(self, name):
        if name in entry_widgets:
            return entry_widgets[name].get()
        else:
            print(f"Warning: Entry '{name}' not found in GUI.")
            return None

    def set_entry(self, name, value):
        if name in entry_widgets:
            root.after(0, lambda: self._set_entry(name, value))
        else:
            print(f"Warning: Entry '{name}' not found in GUI.")

    def _set_entry(self, name, value):
        entry_widgets[name].delete(0, tk.END)
        entry_widgets[name].insert(0, str(value))
        autosave_config()

    def get_list_selection(self, name):
        if name in list_widgets:
            return list_widgets[name].curselection()
        else:
            print(f"Warning: List '{name}' not found in GUI.")
            return None

    def set_list_items(self, name, items):
        if name in list_widgets:
            root.after(0, lambda: self._set_list_items(name, items))
        else:
            print(f"Warning: List '{name}' not found in GUI.")

    def _set_list_items(self, name, items):
        list_widgets[name].delete(0, tk.END)
        for item in items:
            list_widgets[name].insert(tk.END, item)
        autosave_config()

    def set_button_color(self, button_name, color):
        if self.root:
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button) and child.cget('text') == button_name:
                            child.config(bg=color)
                            self.root.update_idletasks()  # Force update of the GUI
                            return
            print(f"Warning: Button '{button_name}' not found.")

    def set_button_text(self, button_name, text):
        if self.root:
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button) and child.cget('text').startswith(button_name):
                            child.config(text=text)
                            self.root.update_idletasks()  # Force update of the GUI
                            return
            print(f"Warning: Button '{button_name}' not found.")

# Add this at the end of the file
g = GUIWrapper()
