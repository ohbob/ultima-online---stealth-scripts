# from py_stealth import *
def main():
    if TargetPresent():
        # ClientPrintEx(LastTarget(), 44, 3, f"LTARGET")
        WaitTargetLast()
        ClientPrintEx(LastTarget(), 44, 3, "↓")