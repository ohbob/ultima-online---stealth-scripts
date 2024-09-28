import time

def main(main_controller):
    start_time = time.time()  # Start timing

    if not TargetPresent():
        friends = main_controller.get_friends()
        if not friends:
            ClientPrintEx(Self(), 1, 3, "No friends in the friendlist.")
            elapsed_time = (time.time() - start_time) * 1000  # Calculate elapsed time in ms
            print(f"Execution time: {elapsed_time:.4f} ms")
            return

        SetFindDistance(12)  # max distance to target
        FindType(0xFFFF, Ground())
        friend_ids = {friend['id'] for friend in friends}  # Use a set for faster lookup
        found_friends = []

        for item in GetFoundList():
            if item in friend_ids:
                hp = GetHP(item)
                if hp > 0 and hp < 25:  # Check HP
                    found_friends.append((item, hp, GetDistance(item)))  # Store item, HP, and distance

        if found_friends:
            # Sort by HP (ascending) and then by distance (ascending)
            closest_friend = min(found_friends, key=lambda x: (x[1], x[2]))[0]
            TargetToObject(closest_friend)
            ClientPrintEx(closest_friend, 65, 3, f"FRIEND")
            ClientPrintEx(closest_friend, 65, 3, "↓")
        else:
            ClientPrintEx(Self(), 1, 3, "No injured friends found nearby.")

    elapsed_time = (time.time() - start_time) * 1000  # Calculate elapsed time in ms
    ClientPrintEx(Self(), 1, 3, f"Execution time: {elapsed_time:.4f} ms")