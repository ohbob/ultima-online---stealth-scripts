from discord_webhook import DiscordWebhook  # pip install discord-webhook
import time

from py_stealth import *

hookurl = 'https://discord.com/api/webhooks/783722507420041216' \
          '/R5Tx8akek9nZebXv2isGqDWK60087lrgzUJ№№№№№№№№###'

# friends = ["Gitana", "Omar"] # если по никам
friends = [0x123456, 0x234567]
shouttime = 60
idtimers = {}
SetFindDistance(30)


def get_character_location(nickname):
    location = {
        "Valdis": "Covetous",
        "maldis": "Britain Entrance",
    }
    return location.get(nickname, "unknown place")


def discosend(message):
    webhook = DiscordWebhook(url=hookurl, content=message)
    webhook.execute()


def findenemy(location):
    global idtimers
    if FindTypesArrayEx([0x0191, 0x0190], [0xFFFF], [Ground()], False):
        for character in GetFoundList():
            # enemy = GetName(character) # если имя
            enemy = character  # если ид
            if enemy not in friends:

                # if first appearance, adding timer
                if enemy not in idtimers:
                    idtimers[enemy] = time.time()
                    discosend(f"{location} : {GetName(character)} has appeared")

                # checking if the enemy name is in dictionary and checking if the historical timer is greater
                if time.time() > idtimers[enemy] + shouttime:
                    # update the new value
                    idtimers[enemy] = time.time()
                    discosend(f"{location} : {GetName(character)} has appeared")


location = get_character_location(GetName(Self()))
Ignore(Self())
while True:
    findenemy(location)
    Wait(1000)
