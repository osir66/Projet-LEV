import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# couleurs
gris = "#3a3a3a"
noir = "#111111"
taille = 300

# variables qu on va utiliser partout
points = []
position = 0
ancien_x = 0
ancien_y = 0
vitesse = 20


# on change la vitesse quand on appuie sur entree
def changer_vitesse(event):
    global vitesse
    try:
        valeur = int(case_vitesse.get())
        if valeur >= 1 and valeur <= 100:
            vitesse = valeur
    except:
        pass


# on adapte les coordonnees du csv a la taille du canvas
def normaliser(liste):
    marge = 20
    tous_les_x = []
    tous_les_y = []
    for x, y, stylo in liste:
        tous_les_x.append(x)
        tous_les_y.append(y)

    petit_x = min(tous_les_x)
    petit_y = min(tous_les_y)
    largeur = max(tous_les_x) - petit_x
    hauteur = max(tous_les_y) - petit_y
    zone = taille - 2 * marge

    nouvelle_liste = []
    for x, y, stylo in liste:
        nouveau_x = marge + (x - petit_x) / largeur * zone
        nouveau_y = marge + (y - petit_y) / hauteur * zone
        nouvelle_liste.append((nouveau_x, nouveau_y, stylo))
    return nouvelle_liste


# on ouvre un fichier csv et on garde les points
def charger():
    global points, position, ancien_x, ancien_y

    chemin = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if chemin == "":
        return

    fichier = open(chemin)
    lignes = fichier.readlines()
    fichier.close()

    # on lit chaque ligne sauf la premiere qui est le nom
    liste = []
    for ligne in lignes[1:]:
        morceaux = ligne.strip().split(";")
        if len(morceaux) >= 4:
            x = float(morceaux[1])
            y = float(morceaux[2])
            stylo = int(morceaux[3])
            liste.append((x, y, stylo))

    points = normaliser(liste)
    position = 0
    canvas.delete("all")

    # on se place sur le premier point
    if len(points) > 0:
        ancien_x = points[0][0]
        ancien_y = points[0][1]
        tracer()


# on trace un point a la fois avec un petit delai
def tracer():
    global position, ancien_x, ancien_y

    # si on a fini on arrete
    if position >= len(points):
        return

    x = points[position][0]
    y = points[position][1]
    stylo = points[position][2]

    # si le stylo est baisse on relie l ancien point au nouveau
    if stylo == 1 and position > 0:
        canvas.create_line(ancien_x, ancien_y, x, y, fill="cyan", width=2)

    # le nouveau point devient l ancien
    ancien_x = x
    ancien_y = y
    position = position + 1

    # plus la vitesse est grande plus le delai est petit
    delai = 110 - vitesse
    if delai < 10:
        delai = 10
    fenetre.after(delai, tracer)


# --- creation de la fenetre ---
fenetre = ctk.CTk()
fenetre.title("Table Tracante LEV")
fenetre.geometry("380x440")
fenetre.configure(fg_color=gris)

# barre du haut avec le bouton charger
barre_haut = ctk.CTkFrame(fenetre, fg_color=gris)
barre_haut.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(barre_haut, text="Fichier", text_color="#cccccc",
             font=("Arial", 11)).pack(side="left")

ctk.CTkButton(barre_haut, text="Charger CSV", width=120,
              fg_color="#555555", hover_color="#666666",
              text_color="white", font=("Arial", 11),
              corner_radius=8, command=charger).pack(side="left", padx=10)

# le canvas ou on dessine
cadre_canvas = ctk.CTkFrame(fenetre, fg_color=noir, corner_radius=12)
cadre_canvas.pack(padx=20, pady=6)

canvas = ctk.CTkCanvas(cadre_canvas, width=taille, height=taille,
                       bg=noir, highlightthickness=0, bd=0)
canvas.pack(padx=8, pady=8)

# barre du bas avec la vitesse
barre_bas = ctk.CTkFrame(fenetre, fg_color=gris)
barre_bas.pack(fill="x", padx=20, pady=10)

ctk.CTkLabel(barre_bas, text="Vitesse", text_color="#cccccc",
             font=("Arial", 11)).pack(side="left")

case_vitesse = ctk.CTkEntry(barre_bas, width=80, font=("Arial", 12),
                            fg_color="#4a4a4a", text_color="white",
                            border_width=0, corner_radius=8,
                            placeholder_text="20")
case_vitesse.pack(side="left", padx=10)
case_vitesse.bind("<Return>", changer_vitesse)

ctk.CTkLabel(barre_bas, text="entree pour valider", text_color="#888888",
             font=("Arial", 10)).pack(side="left")

fenetre.mainloop()