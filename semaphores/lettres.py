from PIL import Image, ImageDraw

# on genere automatiquement n importe quel caractere ASCII depuis ses pixels
def get_lettre(char):
    img = Image.new("1", (12, 12), 0)
    d = ImageDraw.Draw(img)
    d.text((1, 1), char, fill=1)
    grille = []
    for y in range(1, 11):
        ligne = []
        for x in range(1, 11):
            if img.getpixel((x, y)):
                ligne.append((1, 255, 255, 255))
            else:
                ligne.append((0, 0, 0, 0))
        grille.append(ligne)
    return grille

# on construit le dictionnaire avec tous les caracteres ASCII imprimables
LETTRES = {}
for code in range(32, 127):
    LETTRES[chr(code)] = get_lettre(chr(code))