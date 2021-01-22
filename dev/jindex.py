from py_stealth import *
index = HighJournal()
while True:
    while index < HighJournal():
        index = index + 1
        line = Journal(index)
        print(f"sender ID: {LineID()} - {line}") # do whatever you need to do here
    Wait(100)
