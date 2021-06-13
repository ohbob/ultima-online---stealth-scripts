from py_stealth import *


async def onMessage(message):

    split = message.split()
    if len(split) >= 2:
        param = split[1]
    else:
        param = ""

    if "/bark" in split:
        bark()
        return True

    elif "/say" in split:
        say(message.replace("/say", ""))
        return True

    elif '/useskill' in split:
        UseSkill(param)
        return True

    return False




def bark():
    UOSay("Woof")




def say(msg):
    UOSay(msg)
