import tkinter as tk
from tkinter import ttk

class FriendsTab(ttk.Frame):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.friends_listbox = tk.Listbox(self)
        self.friends_listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Friend", command=self.add_friend)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(button_frame, text="Remove Friend", command=self.remove_friend)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear List", command=self.clear_list)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def add_friend(self):
        self.main_controller.add_friend()

    def remove_friend(self):
        selected = self.friends_listbox.curselection()
        if selected:
            friend = self.friends_listbox.get(selected[0])
            self.main_controller.remove_friend(friend)

    def clear_list(self):
        self.main_controller.clear_friends()
        self.populate_list()

    def populate_list(self):
        self.friends_listbox.delete(0, tk.END)
        friends = self.main_controller.get_friends()
        for friend in friends:
            self.friends_listbox.insert(tk.END, friend)