import tkinter as tk
from tkinter import ttk

class FriendsTab:
    def __init__(self, notebook, manager):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Friends")
        self.manager = manager

        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Name'), show='headings')
        self.tree.heading('ID', text='Friend ID')
        self.tree.heading('Name', text='Friend Name')
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=5, padx=10, fill=tk.X)

        ttk.Button(button_frame, text="Add", command=self.add_friend).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove", command=self.remove_friend).pack(side=tk.LEFT, padx=5)

    def load_friends(self, friends):
        self.tree.delete(*self.tree.get_children())
        for friend_id, friend_name in friends:
            self.tree.insert('', 'end', values=(friend_id, friend_name))

    def add_friend(self):
        self.manager.debug("Please select a friend in the game.", "info")
        friend_id = self.manager.getTargetID()
        if friend_id:
            friend_name = self.manager.GetName(friend_id)
            # Check if the friend already exists in the list
            for item in self.tree.get_children():
                if self.tree.item(item)['values'][0] == friend_id:
                    self.manager.debug(f"Friend {friend_name} (ID: {friend_id}) already exists in the list.", "warning")
                    return
            self.tree.insert('', 'end', values=(friend_id, friend_name))
            self.manager.debug(f"Added friend: {friend_name} (ID: {friend_id})", "success")
            self.save_friends()
        else:
            self.manager.debug("Failed to get friend ID.", "error")

    def remove_friend(self):
        selected = self.tree.selection()
        if selected:
            friend_id, friend_name = self.tree.item(selected[0])['values']
            self.tree.delete(selected[0])
            self.manager.debug(f"Removed friend: {friend_name} (ID: {friend_id})", "info")
            self.save_friends()

    def save_friends(self):
        friends = [(self.tree.item(child)['values'][0], self.tree.item(child)['values'][1]) 
                   for child in self.tree.get_children()]
        self.manager.update_friends_list(friends)