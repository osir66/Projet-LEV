from lettres import LETTRES
from helice import extraire_points

points = extraire_points(LETTRES['A'])
for p in points:
    print(p)

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