# from py_stealth import *

def main(main_controller):
    if not TargetPresent():
        friends = main_controller.get_friends()
        if not friends:
            ClientPrintEx(Self(), 1, 3, "No friends in the friendlist.")
            return
        SetFindDistance(12) # max distance to target
        FindType(0xFFFF, Ground())
        found_friends = []
        friend_ids = [friend['id'] for friend in friends]  # Extract friend IDs
        for item in GetFoundList():
            if item in friend_ids:  # Compare by ID
                found_friends.append(item)

        if found_friends:
            closest_friend = min(found_friends, key=lambda x: GetDistance(x))
            TargetToObject(closest_friend)
            ClientPrintEx(closest_friend, 44, 3, f"TARGET")
            ClientPrintEx(closest_friend, 44, 3, "↓")
        else:
            ClientPrintEx(Self(), 1, 3, "No friends found nearby.")