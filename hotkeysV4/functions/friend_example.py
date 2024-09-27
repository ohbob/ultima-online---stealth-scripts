def main(manager):
    friends = manager.get_friends_list()
    manager.debug("Friends list:", "info")
    for friend_id, friend_name in friends:
        manager.debug(f"ID: {friend_id}, Name: {friend_name}", "info")
        # You can add more functionality here, like:
        # SendMessage(friend_id, "Hello, friend!")
        # or any other action you want to perform with friends