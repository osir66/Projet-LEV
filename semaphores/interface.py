import customtkinter as ctk
from lettres import LETTRES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

gris = "#3a3a3a"
noir = "#111111"

# variables globales
lettre_courante = 'A'
grille = LETTRES[lettre_courante]
canvas = None
fenetre = None
label_lettre = None
case_lettre = None


# on change la lettre manuellement depuis le champ texte
def changer_lettre():
    global lettre_courante, grille
    texte = case_lettre.get().upper()
    if texte in LETTRES:
        lettre_courante = texte
        grille = LETTRES[texte]
        label_lettre.configure(text=texte)
        dessiner()


# on change la lettre automatiquement depuis le serveur
def changer_lettre_auto(forme, nom_mission=""):
    global lettre_courante, grille
    if forme in LETTRES:
        lettre_courante = forme
        grille = LETTRES[forme]
        if nom_mission != "":
            label_lettre.configure(text=forme + "  " + nom_mission)
        else:
            label_lettre.configure(text=forme)
        dessiner()

# on efface le canvas quand il n y a plus de mission
def vider():
    canvas.delete("all")
    label_lettre.configure(text="")

# on dessine la lettre au centre du canvas 300x300
def dessiner():
    canvas.delete("all")
    taille_led = 15
    nb_colonnes = len(grille[0])
    nb_lignes = len(grille)
    centre_x = 150
    centre_y = 150
    debut_x = centre_x - nb_colonnes * taille_led // 2
    debut_y = centre_y - nb_lignes * taille_led // 2

    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes):
            led = grille[ligne][colonne]
            if led[0] == 1:
                x = debut_x + colonne * taille_led + taille_led // 2
                y = debut_y + ligne * taille_led + taille_led // 2
                couleur = f'#{led[1]:02x}{led[2]:02x}{led[3]:02x}'
                canvas.create_oval(x - 5, y - 5, x + 5, y + 5,
                                   fill=couleur, outline='')


# boucle qui rafraichit l affichage
def animer():
    dessiner()
    fenetre.after(100, animer)


# on cree tous les widgets dans la fenetre passee en parametre
def lancer(root):
    global canvas, fenetre, label_lettre, case_lettre

    fenetre = root
    fenetre.title("Semaphore LEV")
    fenetre.geometry("380x440")
    fenetre.configure(fg_color=gris)
    fenetre.resizable(True, True)

    # barre du haut
    barre_haut = ctk.CTkFrame(fenetre, fg_color=gris)
    barre_haut.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(barre_haut, text="Symbole", text_color="#cccccc",
                 font=("Arial", 11)).pack(side="left")

    case_lettre = ctk.CTkEntry(barre_haut, width=80, font=("Arial", 13, "bold"),
                               fg_color="#4a4a4a", text_color="white",
                               border_width=0, corner_radius=8)
    case_lettre.insert(0, 'A')
    case_lettre.pack(side="left", padx=10)

    ctk.CTkButton(barre_haut, text="Afficher", width=90,
                  fg_color="#555555", hover_color="#666666",
                  text_color="white", font=("Arial", 11),
                  corner_radius=8, command=changer_lettre).pack(side="left")

    label_lettre = ctk.CTkLabel(barre_haut, text="A", text_color="#aaaaaa",
                                 font=("Arial", 11), fg_color=gris)
    label_lettre.pack(side="right")

    # canvas
    cadre_canvas = ctk.CTkFrame(fenetre, fg_color=noir, corner_radius=12)
    cadre_canvas.pack(padx=20, pady=6)

    canvas = ctk.CTkCanvas(cadre_canvas, width=300, height=300,
                           bg=noir, highlightthickness=0, bd=0)
    canvas.pack(padx=8, pady=8)

    # barre du bas
    barre_bas = ctk.CTkFrame(fenetre, fg_color=gris)
    barre_bas.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(barre_bas, text="Symbole actif", text_color="#888888",
                 font=("Arial", 10)).pack(side="left")

    animer()


# si on lance interface.py directement
if __name__ == "__main__":
    root = ctk.CTk()
    lancer(root)
    root.mainloop()