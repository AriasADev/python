# Pseudocode
# stored_pass <- "password"
# password <- ""
# pass_mismatch <- stored_pass != password

# WHILE pass_mismatch
#     OUTPUT "Enter your password:"
#     password <- USERINPUT
#     pass_mismatch <- stored_pass != password
# END WHILE

# OUTPUT "Access granted"

import os
import sys

devMode = False  # Set to False to allow self-deletion

def selfDestruct(devMode=False):
    if not devMode:
        scriptPath = os.path.abspath(__file__)
        os.remove(scriptPath)
    sys.exit()

storedPass = "password"
attempts = 0
maxAttempts = 3

while attempts < maxAttempts:
    password = input("Enter yer fuckin' password, ya daftie: ")

    if storedPass == password:
        print("Aye, access granted, ye absolute legend!: ")
        break
    else:
        attempts += 1
        print("Fuck right off, ye wee cunt, ye've got the fucking password wrong, ya wank!: ")
if attempts == maxAttempts:
    print("Right, that's enough. Ye've fucked it now. Get lost!")
    selfDestruct(devMode)
