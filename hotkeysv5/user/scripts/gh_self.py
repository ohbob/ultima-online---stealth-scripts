# from py_stealth import *
def main():
    Cast("Greater Heal")
    WaitForTarget(2000)
    if TargetPresent():
        TargetToObject(Self())
    # ... rest of your script