import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# couleurs et taille du canvas
gris = "#3a3a3a"
noir = "#111111"
taille = 300

# variables qu on va utiliser partout
points = []
position = 0
ancien_x = 0
ancien_y = 0
vitesse = 20
canvas = None
fenetre_tt = None


def changer_vitesse(valeur):
    """met a jour la vitesse de tracage quand on bouge la jauge
    plus la jauge est basse plus le trace est lent"""
    global vitesse
    vitesse = int(float(valeur))


def normaliser(liste):
    """adapte les coordonnees du csv a la taille reelle du canvas 300x300
    en gardant les proportions et une marge sur les bords"""
    marge = 20

    tous_les_x = [p[0] for p in liste]
    tous_les_y = [p[1] for p in liste]
    petit_x = min(tous_les_x)
    petit_y = min(tous_les_y)
    largeur = max(tous_les_x) - petit_x
    hauteur = max(tous_les_y) - petit_y

    zone = taille - 2 * marge

    result = []
    for x, y, stylo in liste:
        nx = marge + (x - petit_x) / largeur * zone
        ny = marge + (y - petit_y) / hauteur * zone
        result.append((nx, ny, stylo))
    return result


def charger():
    """ouvre une fenetre pour choisir un fichier csv sur l ordinateur
    et lance le chargement de son contenu"""
    chemin = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if chemin == "":
        return
    fichier = open(chemin)
    texte = fichier.read()
    fichier.close()
    charger_depuis_texte(texte)


def charger_depuis_texte(texte):
    """lit un texte au format csv venant du fichier ou du serveur
    extrait les points x y stylo et lance le tracage"""
    global points, position, ancien_x, ancien_y

    texte = texte.replace("\r\n", "\n").replace("\r", "\n")

    lignes = texte.strip().split("\n")

    premiere = lignes[0].strip().split(";")
    if len(premiere) >= 4:
        debut = 0
    else:
        debut = 1

    liste = []
    for ligne in lignes[debut:]:
        morceaux = ligne.strip().split(";")
        if len(morceaux) >= 4:
            x = float(morceaux[1])
            y = float(morceaux[2])
            stylo_brut = morceaux[3].strip()
            stylo = int(stylo_brut[0]) if stylo_brut else 0
            liste.append((x, y, stylo))

    if len(liste) == 0:
        return

    points = normaliser(liste)
    position = 0
    canvas.delete("all")

    ancien_x = points[0][0]
    ancien_y = points[0][1]
    tracer()


def tracer():
    """trace un point a la fois en reliant les points avec le stylo baisse
    se rappelle elle meme jusqu a la fin puis remet le stylo au repos"""
    global position, ancien_x, ancien_y

    if position >= len(points):
        x0 = taille
        y0 = 0
        canvas.delete("rail")
        canvas.create_line(0, y0, taille, y0, fill="#666666", width=2, tags="rail")
        canvas.create_line(x0, 0, x0, taille, fill="#666666", width=2, tags="rail")
        canvas.delete("stylo")
        canvas.create_oval(x0 - 5, y0 - 5, x0 + 5, y0 + 5,
                           fill="red", outline="", tags="stylo")
        return

    x = points[position][0]
    y = points[position][1]
    stylo = points[position][2]

    if stylo == 1 and position > 0:
        canvas.create_line(ancien_x, ancien_y, x, y, fill="cyan", width=2)

    ancien_x = x
    ancien_y = y
    position = position + 1

    canvas.delete("rail")
    canvas.create_line(0, y, taille, y, fill="#666666", width=2, tags="rail")
    canvas.create_line(x, 0, x, taille, fill="#666666", width=2, tags="rail")

    canvas.delete("stylo")
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                       fill="red", outline="", tags="stylo")

    delai = int(500 - vitesse * 4)
    if delai < 10:
        delai = 10
    fenetre_tt.after(delai, tracer)


def lancer(root):
    """construit toute l interface bouton charger canvas et jauge
    dans la fenetre recue en parametre"""
    global canvas, fenetre_tt

    fenetre_tt = root
    fenetre_tt.title("Table Tracante LEV")
    fenetre_tt.geometry("380x440")
    fenetre_tt.configure(fg_color=gris)

    barre_haut = ctk.CTkFrame(fenetre_tt, fg_color=gris)
    barre_haut.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(barre_haut, text="Fichier", text_color="#cccccc",
                 font=("Arial", 11)).pack(side="left")

    ctk.CTkButton(barre_haut, text="Charger CSV", width=120,
                  fg_color="#555555", hover_color="#666666",
                  text_color="white", font=("Arial", 11),
                  corner_radius=8, command=charger).pack(side="left", padx=10)

    cadre_canvas = ctk.CTkFrame(fenetre_tt, fg_color=noir, corner_radius=12)
    cadre_canvas.pack(padx=20, pady=6)

    canvas = ctk.CTkCanvas(cadre_canvas, width=taille, height=taille,
                           bg=noir, highlightthickness=0, bd=0)
    canvas.pack(padx=8, pady=8)

    barre_bas = ctk.CTkFrame(fenetre_tt, fg_color=gris)
    barre_bas.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(barre_bas, text="Vitesse", text_color="#cccccc",
                 font=("Arial", 11)).pack(side="left")

    jauge_vitesse = ctk.CTkSlider(barre_bas, from_=1, to=100,
                                   command=changer_vitesse)
    jauge_vitesse.set(20)
    jauge_vitesse.pack(side="left", padx=10, fill="x", expand=True)


if __name__ == "__main__":
    root = ctk.CTk()
    lancer(root)
    root.mainloop()