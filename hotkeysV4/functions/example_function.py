def debug(message, level="info"):
    print(f"[{level.upper()}] {message}")

def main(ctx):
    debug(ctx)
    debug("Example function called", "info")
    UOSay("Yes sir")
    while GetHP(Self())<MaxHP():
        Cast("Greater Heal")
        WaitForTarget(2500)
        if TargetPresent():
            TargetToObject(Self())
