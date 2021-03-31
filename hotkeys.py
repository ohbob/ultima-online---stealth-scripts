from py_stealth import *
from pynput import keyboard


def F1():
    CastToObject('Magic Arrow', Self())


def F2():
    CastToObject('Magic Arrow', LastTarget())


with keyboard.GlobalHotKeys({
    '<f1>': F1,
    '<f2>': F2
}) as h:
    h.join()
