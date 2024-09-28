from py_stealth import *
# print(IsActiveSpellAbility('double strike'))

SetFindDistance = 50

# for _ in range(2):
#     FindType(0x0191, Ground())
#     print(f"Iteration {_}")
#     for item in GetFindedList():
#         ClientPrintEx(Self(), 123, 1, GetName(item))
#         print(GetName(item))
#         Ignore(item)

#     Wait(1000)  # Small delay between iterations

ClientPrintEx(Self(), 123, 1, f"Lightning strike {IsActiveSpellAbility('lightning strike')}")


# print(GetActiveAbility())
# UsePrimaryAbility()
# Wait(200)
# print(GetActiveAbility())
# Wait(200)
# UseSecondaryAbility()
# Wait(200)
# print(GetActiveAbility())


# if Mana() > 25 and GetActiveAbility() not in ["Double Strike"]:
# #     print("Using primary")
# #     UsePrimaryAbility()


# GetActiveAbility()