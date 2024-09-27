class FriendsController:
    def __init__(self, state):
        self.state = state
        self.friends = []

    def add_friend(self, friend):
        self.friends.append(friend)
        self.state.update_friends(self.friends)

    def remove_friend(self, friend):
        if friend in self.friends:
            self.friends.remove(friend)
            self.state.update_friends(self.friends)

    def get_friends(self):
        return self.friends

    # Add other friend-related methods