# from py_stealth import *
def main():
    if TargetPresent():
        # ClientPrintEx(LastTarget(), 44, 3, f"LTARGET")
        TargetToObject(LastTarget())
        ClientPrintEx(LastTarget(), 44, 3, "↓")