import customtkinter as ctk
from tkinter import filedialog
from math import sin, cos, radians, hypot, atan2, degrees

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# couleurs et taille du canvas
gris = "#3a3a3a"
noir = "#111111"
taille = 300
centre = taille // 2

# variables qu on va utiliser partout
matrice = [[None for _ in range(10)] for _ in range(360)]
vitesse = 20
angle = 0
remanents = []
canvas = None
fenetre_h = None


def changer_vitesse(valeur):
    """met a jour la vitesse de rotation quand on bouge la jauge
    plus la jauge est basse plus l helice tourne lentement"""
    global vitesse
    vitesse = int(float(valeur))


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
    """lit un csv polaire rayon angle etat le convertit en cartesien
    puis remplit la matrice qui sert a allumer les leds pendant la rotation"""
    global matrice, angle, remanents

    texte = texte.replace("\r\n", "\n").replace("\r", "\n")

    lignes = texte.strip().split("\n")
    premiere = lignes[0].strip().split(";")
    debut = 0 if len(premiere) >= 4 else 1

    sommets_polaire = []
    for ligne in lignes[debut:]:
        morceaux = ligne.strip().split(";")
        if len(morceaux) >= 4:
            r = float(morceaux[1])
            a = float(morceaux[2])
            stylo_brut = morceaux[3].strip()
            stylo = int(stylo_brut[0]) if stylo_brut else 0
            sommets_polaire.append((r, a, stylo))

    if not sommets_polaire:
        return

    # x = rayon fois cosinus de l angle
    # y = moins rayon fois sinus de l angle pour remettre le haut en haut
    cartesien = []
    for r, a, stylo in sommets_polaire:
        x = r * cos(radians(a))
        y = -r * sin(radians(a))
        cartesien.append((x, y, stylo))

    xs = [p[0] for p in cartesien]
    ys = [p[1] for p in cartesien]
    mx = (max(xs) + min(xs)) / 2
    my = (max(ys) + min(ys)) / 2
    pts_centres = [(x - mx, y - my, s) for x, y, s in cartesien]

    r_max = max(hypot(x, y) for x, y, s in pts_centres)
    if r_max == 0:
        return

    segments = []
    for i in range(1, len(pts_centres)):
        x0, y0, s0 = pts_centres[i - 1]
        x1, y1, s1 = pts_centres[i]
        if s1 == 1:
            segments.append((x0, y0, x1, y1))

    # pour chaque angle possible de la branche on regarde si elle croise
    # un segment de la forme et a quelle distance du centre
    matrice = [[None for _ in range(10)] for _ in range(360)]
    for theta in range(360):
        dx = cos(radians(theta))
        dy = sin(radians(theta))
        for ax, ay, bx, by in segments:
            ex = bx - ax
            ey = by - ay
            denom = dx * ey - dy * ex
            if abs(denom) < 1e-10:
                continue
            t = (ax * ey - ay * ex) / denom
            s = (ax * dy - ay * dx) / denom
            if t > 0.5 and 0 <= s <= 1:
                led = min(9, int(t / r_max * 9))
                matrice[theta][led] = (0, 255, 255)

    canvas.delete("all")
    angle = 0
    remanents = []


def animer():
    """fait tourner les quatre branches et allume les leds prevues par la matrice
    gere aussi l extinction progressive des pixels deja allumes"""
    global angle

    for p in remanents[:]:
        p["vie"] = p["vie"] - 25
        if p["vie"] <= 0:
            canvas.delete(p["id"])
            remanents.remove(p)
        else:
            ratio = p["vie"] / 255.0
            vert = int(255 * ratio)
            canvas.itemconfig(p["id"], fill=f'#00{vert:02x}{vert:02x}')

    canvas.delete("branche")

    # plus vitesse est grand plus on avance de degres a chaque tour
    pas = 1 + vitesse // 5

    for indice_pas in range(pas):
        angle = (angle + 1) % 360
        dernier_pas = (indice_pas == pas - 1)

        for b in range(4):
            angle_branche = (angle + b * 90) % 360
            ar = radians(angle_branche)

            if dernier_pas:
                canvas.create_line(centre, centre,
                                   centre + 130 * cos(ar),
                                   centre + 130 * sin(ar),
                                   fill="#444444", width=2, tags="branche")

            for i in range(10):
                if matrice[angle_branche][i] is not None:
                    r_phys = (i + 1) * 12
                    x = centre + r_phys * cos(ar)
                    y = centre + r_phys * sin(ar)
                    tid = canvas.create_oval(x - 3, y - 3, x + 3, y + 3,
                                            fill="cyan", outline="")
                    remanents.append({"id": tid, "vie": 255})

    delai = int(220 - vitesse * 2)
    if delai < 5:
        delai = 5
    fenetre_h.after(delai, animer)


def lancer(root):
    """construit toute l interface bouton charger canvas et jauge
    dans la fenetre recue en parametre"""
    global canvas, fenetre_h

    fenetre_h = root
    fenetre_h.title("Helice POV LEV")
    fenetre_h.geometry("380x470")
    fenetre_h.configure(fg_color=gris)

    barre_haut = ctk.CTkFrame(fenetre_h, fg_color=gris)
    barre_haut.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(barre_haut, text="Fichier", text_color="#cccccc",
                 font=("Arial", 11)).pack(side="left")

    ctk.CTkButton(barre_haut, text="Charger CSV", width=120,
                  fg_color="#555555", hover_color="#666666",
                  text_color="white", font=("Arial", 11),
                  corner_radius=8, command=charger).pack(side="left", padx=10)

    cadre_canvas = ctk.CTkFrame(fenetre_h, fg_color=noir, corner_radius=12)
    cadre_canvas.pack(padx=20, pady=6)

    canvas = ctk.CTkCanvas(cadre_canvas, width=taille, height=taille,
                           bg=noir, highlightthickness=0, bd=0)
    canvas.pack(padx=8, pady=8)

    barre_bas = ctk.CTkFrame(fenetre_h, fg_color=gris)
    barre_bas.pack(fill="x", padx=20, pady=10)

    ctk.CTkLabel(barre_bas, text="Vitesse", text_color="#cccccc",
                 font=("Arial", 11)).pack(side="left")

    jauge_vitesse = ctk.CTkSlider(barre_bas, from_=1, to=100,
                                   command=changer_vitesse)
    jauge_vitesse.set(20)
    jauge_vitesse.pack(side="left", padx=10, fill="x", expand=True)

    animer()


if __name__ == "__main__":
    root = ctk.CTk()
    lancer(root)
    root.mainloop()