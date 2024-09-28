# from py_stealth import *
def main():
    if IsPoisoned(Self()):
        Cast("Cure")
        WaitForTarget(2000)
        if TargetPresent():
            TargetToObject(Self())
            Wait(1000)