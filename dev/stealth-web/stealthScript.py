import random
from datetime import datetime

from py_stealth import *

index = HighJournal()

player = {}
journal = []
log = ["one", "two"]

stats = {
    0x001: {
        'name': 'iron',
        'amount': 151
    },
    0x002: {
        'name': 'dullcopper',
        'amount': 123
    },
    0x003: {
        'name': 'shadow',
        'amount': 151
    },
    0x004: {
        'name': 'copper',
        'amount':61
    },
    0x005: {
        'name': 'bronze',
        'amount': 412
    },
    0x006: {
        'name': 'golden',
        'amount': 13
    },
    0x007: {
        'name': 'agapite',
        'amount': 66
    },
    0x008: {
        'name': 'verite',
        'amount': 96
    },
    0x009: {
        'name': 'valorite',
        'amount': 15
    },
}


def updateobject():
    player['name'] = GetName(Self())
    player['hp'] = HP()
    player['maxhp'] = MaxHP()
    player['mana'] = Mana()
    player['maxmana'] = MaxMana()
    player['stam'] = Stam()
    player['maxstam'] = MaxStam()
    player['X'] = GetX(Self())
    player['Y'] = GetY(Self())
    player['profilename'] = ProfileName()
    player['shardname'] = ShardName()
    player['connected'] = Connected()
    player['clientversion'] = GetClientVersionInt()


def updatejournal():
    entriestokeep = 1000
    global index
    global journal
    while index < HighJournal():
        index = index + 1
        line = Journal(index)
        journal = journal[-entriestokeep:]
        journal.append(line)
        log.append(random.random())
        # print(f"sender ID: {LineID()} - {line}")  # do whatever you need to do here
