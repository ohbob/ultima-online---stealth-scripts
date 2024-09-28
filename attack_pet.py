from py_stealth import *

while True:
    if Mana() > 30:
        CastToObj('word of death', 0x001C9B87)
        Wait(1000)
