from core.uo_globals import debug, getTargetID

class FriendsController:
    def __init__(self, state, py_stealth):
        self.state = state
        self.py_stealth = py_stealth

    def add_friend(self):
        debug(self.py_stealth, "Select a friend to add")
        target_id = getTargetID(self.py_stealth)
        if target_id:
            name = self.py_stealth.GetName(target_id)
            if not name and self.py_stealth.GetHP(target_id) <= 0:
                debug(self.py_stealth, "Target is not a player or is dead", "fail")
                return
            if any(friend['id'] == target_id for friend in self.state.friends):
                debug(self.py_stealth, f"Friend {name} is already in the list", "fail")
            else:
                friend = {'name': name, 'id': target_id}
                self.state.friends.append(friend)
                self.state.update_friends(self.state.friends)
                debug(self.py_stealth, f"Added friend: {name}, {target_id}", "success")
        else:
            debug(self.py_stealth, "No target selected")

    def remove_friend(self, id):
        friend_to_remove = next((friend for friend in self.state.friends if friend['id'] == id), None)
        if friend_to_remove:
            self.state.friends.remove(friend_to_remove)
            self.state.update_friends(self.state.friends)
            debug(self.py_stealth, f"Removed friend: {friend_to_remove['name']}, {id}", "success")
        else:
            debug(self.py_stealth, f"No friend with id {id} found", "fail")

    def clear_friends(self):
        self.state.friends = []
        self.state.update_friends(self.state.friends)

    def get_friends(self):
        return self.state.friends