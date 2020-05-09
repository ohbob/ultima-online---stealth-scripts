''' Script Name: Master & Slave
 Author: Camo
 Version: 0.1 Beta
 Client Tested with: 7.0.85.15
 Stealth version tested with: 8.10.2
 Shard OSI: https://uo.com/
 Revision Date: 2020/05/04
 Public Release: 2020/05/04
 Notes: Purpose ir to control slave accounts from master account. They follow master who makes a party and two other accouunts make a party then all the slaves follow the master who
 Revision. 0.1 --
'''

from py_stealth import *
from datetime import datetime

main_host = "Darth"  # Phat Man
party2_host = "Host2"
party3_host = "Host3"

party1 = [0x06396E7E, 0x06396E7E]
party2 = [0x06396E7E, 0x06396E7E]
party3 = [0x06396E7E, 0x06396E7E]


def Host(party):
    for id in party:
        if IsObjectExists(id):
            InviteToParty(id)
            CheckLag()


def Slave(id):
    slavemessages = ["all follow me", "all guard"]
    while True:
        for message in slavemessages:
            UOSay(message)
            Wait(500)

        partyaccepted = False
        while not partyaccepted:
            beforeaction = datetime.now()
            if WaitJournalLine(beforeaction, "Type /accept to join or /decline to decline", 12000):
                PartyAcceptInvite()
                partyaccepted = True

        while not Dead():
            if GetDistance(id) > 1:
                NewMoveXY(GetX(id), GetY(id), True, 1, True)
            Wait(50)

        while Dead():
            Wait(1000)


# ----------------- MAIN LOOP -----------------

# ------ Check if you are the host
ClickOnObject(Self())
if CheckLag(20000):
    if GetName(Self()).lower() in main_host.lower():
        Host(party1)
    elif GetName(Self()).lower() in party2_host.lower():
        Host(party2)
    elif GetName(Self()).lower() in party2_host.lower():
        Host(party3)

    else:
        # ------ Check for slaves
        SetFindVertical(20)
        SetFindDistance(20)
        while True:
            FindType(0x025E, Ground())  # 0x0190 for man, 0x0191 for woman
            foundlist = GetFindedList()
            for potentialhost in foundlist:
                if CheckLag(20000):
                    ClickOnObject(potentialhost)
                    CheckLag()
                    if GetName(potentialhost).lower() in main_host.lower():
                        Slave(potentialhost)
            Wait(1000)

# ----------------- END LOOP -----------------