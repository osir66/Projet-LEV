import customtkinter as ctk
from tkinter import filedialog
from math import sin, cos, radians, hypot, atan2, degrees

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# couleurs
gris = "#3a3a3a"
noir = "#111111"
taille = 540

# variables qu on va utiliser partout
points = []
angle = 0
vitesse = 3
angle_avant = [0, 90, 180, 270]


# on change la vitesse quand on appuie sur entree
def changer_vitesse(event):
    global vitesse
    try:
        valeur = float(case_vitesse.get())
        if valeur > 0 and valeur <= 15:
            vitesse = valeur
    except:
        pass


# on ouvre un fichier csv et on prepare les points
def charger():
    chemin = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if chemin == "":
        return
    fichier = open(chemin)
    texte = fichier.read()
    fichier.close()
    preparer(texte)


# on transforme le csv en points avec un rayon et un angle
def preparer(texte):
    global points, angle, angle_avant

    # on lit chaque ligne sauf la premiere qui est le nom
    sommets = []
    lignes = texte.strip().split("\n")
    for ligne in lignes[1:]:
        morceaux = ligne.strip().split(";")
        if len(morceaux) >= 4:
            x = float(morceaux[1])
            y = float(morceaux[2])
            stylo = int(morceaux[3])
            sommets.append((x, y, stylo))

    # on ajoute des points entre les sommets pour faire des lignes pleines
    bruts = []
    ancien = None
    for x, y, stylo in sommets:
        if stylo == 1 and ancien is not None:
            ancien_x = ancien[0]
            ancien_y = ancien[1]
            distance = hypot(x - ancien_x, y - ancien_y)
            nombre = int(distance * 4)
            if nombre < 2:
                nombre = 2
            # on glisse de l ancien point vers le nouveau
            for i in range(nombre + 1):
                t = i / nombre
                point_x = ancien_x + (x - ancien_x) * t
                point_y = ancien_y + (y - ancien_y) * t
                bruts.append((point_x, point_y))
        ancien = (x, y)

    if len(bruts) == 0:
        return

    # on cherche le centre du dessin
    tous_les_x = []
    tous_les_y = []
    for x, y in bruts:
        tous_les_x.append(x)
        tous_les_y.append(y)
    milieu_x = (max(tous_les_x) + min(tous_les_x)) / 2
    milieu_y = (max(tous_les_y) + min(tous_les_y)) / 2

    # on calcule de combien agrandir le dessin
    largeur = max(tous_les_x) - min(tous_les_x)
    hauteur = max(tous_les_y) - min(tous_les_y)
    plus_grand = max(largeur, hauteur, 1)
    echelle = 240 / plus_grand

    # on transforme chaque point en rayon et angle
    points = []
    for x, y in bruts:
        centre_x = (x - milieu_x) * echelle
        centre_y = (y - milieu_y) * echelle
        rayon = hypot(centre_x, centre_y)
        angle_point = degrees(atan2(centre_y, centre_x)) % 360
        points.append((rayon, angle_point))

    canvas.delete("all")
    angle = 0
    angle_avant = [0, 90, 180, 270]


# appelee par le serveur quand le semaphore est une helice
def charger_depuis_texte(texte):
    preparer(texte)


# on allume une led puis on la supprime apres un court instant
def allumer_led(x, y):
    led = canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="cyan", outline="")
    fenetre.after(120, lambda: canvas.delete(led))


# boucle qui fait tourner les branches
def animer():
    global angle, angle_avant

    angle = angle + vitesse
    centre = taille // 2

    # on efface les anciennes branches
    canvas.delete("branche")

    # on a 4 branches separees de 90 degres
    for b in range(4):
        angle_branche = (angle + b * 90) % 360
        radian = radians(angle_branche)

        # on dessine la branche
        bout_x = centre + 250 * cos(radian)
        bout_y = centre + 250 * sin(radian)
        canvas.create_line(centre, centre, bout_x, bout_y,
                           fill="#444444", width=2, tags="branche")

        # on regarde tous les points
        avant = angle_avant[b] % 360
        for rayon, angle_point in points:
            pas_branche = (angle_branche - avant) % 360
            pas_point = (angle_point - avant) % 360
            # si la branche vient de passer sur le point on l allume
            if pas_point >= 0 and pas_point <= pas_branche:
                x = centre + rayon * cos(radians(angle_point))
                y = centre + rayon * sin(radians(angle_point))
                allumer_led(x, y)

        angle_avant[b] = angle + b * 90

    fenetre.after(16, animer)


# --- creation de la fenetre ---
fenetre = ctk.CTk()
fenetre.title("Helice POV LEV")
fenetre.geometry("620x680")
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
                            placeholder_text="3")
case_vitesse.pack(side="left", padx=10)
case_vitesse.bind("<Return>", changer_vitesse)

ctk.CTkLabel(barre_bas, text="entree pour valider", text_color="#888888",
             font=("Arial", 10)).pack(side="left")

animer()
fenetre.mainloop()