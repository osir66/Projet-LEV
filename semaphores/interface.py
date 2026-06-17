import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# couleurs de la fenetre et du canvas
gris = "#3a3a3a"
noir = "#111111"

# variables qu on va utiliser partout
caractere = "A"
canvas = None
fenetre = None
label_lettre = None
case_lettre = None


def changer_lettre():
    """recupere le texte tape dans la case et affiche son premier caractere"""
    global caractere
    texte = case_lettre.get()
    if len(texte) > 0:
        caractere = texte[0]
        label_lettre.configure(text=caractere)
        dessiner()


def changer_lettre_auto(forme, nom_mission=""):
    """change le caractere affiche automatiquement quand une mission arrive du serveur"""
    global caractere
    if len(forme) > 0:
        caractere = forme[0]
        if nom_mission != "":
            label_lettre.configure(text=caractere + "  " + nom_mission)
        else:
            label_lettre.configure(text=caractere)
        dessiner()


def vider():
    """efface le canvas et le label quand il n y a plus de mission a afficher"""
    canvas.delete("all")
    label_lettre.configure(text="")


def dessiner():
    """affiche le caractere ascii en grand au centre du canvas"""
    canvas.delete("all")
    canvas.create_text(150, 150, text=caractere,
                       fill="white", font=("Courier", 120, "bold"))


def animer():
    """boucle qui redessine le caractere toutes les 500 millisecondes
    elle s arrete proprement si la fenetre a ete fermee"""
    try:
        if fenetre and fenetre.winfo_exists():
            dessiner()
            fenetre.after(500, animer)
    except:
        pass


def lancer(root):
    """construit tous les boutons et le canvas dans la fenetre recue en parametre"""
    global canvas, fenetre, label_lettre, case_lettre

    fenetre = root
    fenetre.title("Semaphore LEV")
    fenetre.geometry("380x440")
    fenetre.configure(fg_color=gris)
    fenetre.resizable(True, True)

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

    cadre_canvas = ctk.CTkFrame(fenetre, fg_color=noir, corner_radius=12)
    cadre_canvas.pack(padx=20, pady=6)

    canvas = ctk.CTkCanvas(cadre_canvas, width=300, height=300,
                           bg=noir, highlightthickness=0, bd=0)
    canvas.pack(padx=8, pady=8)

    barre_bas = ctk.CTkFrame(fenetre, fg_color=gris)
    barre_bas.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(barre_bas, text="Symbole actif", text_color="#888888",
                 font=("Arial", 10)).pack(side="left")

    animer()


if __name__ == "__main__":
    root = ctk.CTk()
    lancer(root)
    root.mainloop()