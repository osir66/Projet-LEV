from lettres import LETTRES

lettre = LETTRES['A']

for ligne in lettre:
    for led in ligne:
        if led[0] == 1:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
    

print("----------------------")


lettress = LETTRES['B']

for ligne in lettress:
    for led in ligne:
        if led[0] == 1:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()