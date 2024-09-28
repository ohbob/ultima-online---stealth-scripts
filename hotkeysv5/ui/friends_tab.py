import tkinter as tk
from tkinter import ttk, messagebox

class FriendsTab(ttk.Frame):
    def __init__(self, parent, main_controller):
        super().__init__(parent)
        self.main_controller = main_controller
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Name', 'ID'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('ID', text='ID')
        self.tree.column('Name', width=150)
        self.tree.column('ID', width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Friend", command=self.add_friend)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = ttk.Button(button_frame, text="Remove Friend", command=self.remove_friend)
        self.remove_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear Friends", command=self.clear_friends)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        friends = self.main_controller.get_friends()
        for friend in friends:
            self.tree.insert('', 'end', values=(friend['name'], friend['id']))

    def add_friend(self):
        self.main_controller.add_friend()

    def remove_friend(self):
        selected_item = self.tree.selection()
        if selected_item:
            friend_id = self.tree.item(selected_item)['values'][1]
            self.main_controller.remove_friend(friend_id)

    def clear_friends(self):
        if messagebox.askyesno("Clear Friends", "Are you sure you want to clear all friends?"):
            self.main_controller.clear_friends()

    # ... (other methods)