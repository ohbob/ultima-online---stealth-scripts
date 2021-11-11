from py_stealth import *
from discord.ext import commands
# https://github.com/Rapptz/discord.py
# https://www.writebots.com/discord-bot-token/


from key import key

# key = '########################'

bot = commands.Bot(command_prefix='!')
gatelist = list(range(0, 102, 6))  # 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90, 96


def getrunes() -> list:
    runebooks = []
    if FindType(0x22C5, Backpack()):
        for found in GetFindedList():
            UseObject(found)
            while GetGumpsCount() == 0:
                Wait(100)
            for i in range(0, GetGumpsCount()):
                gump = GetGumpID(i)
                if gump == 1431013363:  # runebook gump id
                    book = [found]
                    entries = GetGumpInfo(i)['Text'][2:18]  # runes 1 to 16
                    for entry in entries:
                        book.append(entry[0])
                    NumGumpButton(i, 0)
                    Wait(500)
                    CheckLag(10000)
                    print(f"Found: {book}")
                    runebooks.append(book)
    return runebooks


async def opengate(runebooklist: list, location: str) -> bool:
    for i, rb in enumerate(runebooklist):
        for n, name in enumerate(rb):
            if location.upper() in str(name).upper():
                print(str(name).upper())
                runebook_id = runebooklist[i][0]
                runebook_rune = n
                print(f"{runebook_id} {runebook_rune}")
                while GetGumpsCount() > 0:
                    for e in range(0, GetGumpsCount()):
                        CloseSimpleGump(e)
                        CheckLag(500)
                    Wait(500)
                gated = False
                cnt = 1
                while not gated:
                    if cnt > 10:
                        return False
                    UseObject(runebook_id)
                    while GetGumpsCount() == 0:
                        Wait(1000)
                    for c in range(0, GetGumpsCount()):
                        gump = GetGumpID(c)
                        if gump == 1431013363:  # runebook gump id
                            NumGumpButton(c, gatelist[runebook_rune])
                            Wait(4000)
                        if FindTypesArrayEx([0x0F6C, 0x0DDA], [0xFFFF], [Ground()], False) > 0:
                            return True
                    Wait(1000)
                    cnt += 1


rbs = getrunes()


@bot.event
async def on_ready():
    print('Logged in as: ' + bot.user.name)
    print('Ready!\n')


@bot.command()
async def gate(ctx, runename: str = None):
    if runename is not None:
        try:
            if await opengate(rbs, runename):
                await(ctx.send(f"Opened a gate to {runename}"))
        except ValueError:
            await(ctx.send("something went wrong"))


bot.run(key)
