def debug(message, level="info"):
    print(f"[{level.upper()}] {message}")

def main(manager=None):
    debug("Example function called", "info")
    UOSay("Yes sir")