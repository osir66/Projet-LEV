import customtkinter as ctk
from tkinter import filedialog
from math import sin, cos, radians, hypot, atan2, degrees

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

gris = "#3a3a3a"
noir = "#111111"
taille = 300
centre = taille // 2

matrice = [[None for _ in range(10)] for _ in range(360)]
vitesse = 5
angle = 0
remanents = []
canvas = None
fenetre_h = None


def changer_vitesse(valeur):
    global vitesse
    vitesse = int(float(valeur))
    if vitesse < 1:
        vitesse = 1


def charger():
    chemin = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    if chemin == "":
        return
    fichier = open(chemin)
    texte = fichier.read()
    fichier.close()
    charger_depuis_texte(texte)


def charger_depuis_texte(texte):
    global matrice, angle, remanents
    
    texte_propre = texte.replace(" ", "\n").strip()
    
    points_bruts = []
    for ligne in texte_propre.split("\n")[1:]:
        morceaux = ligne.strip().split(";")
        if len(morceaux) >= 4:
            x = float(morceaux[1])
            y = float(morceaux[2])
            stylo = int(morceaux[3])
            points_bruts.append((x, y, stylo))
            
    if not points_bruts:
        return

    tous_les_x = [p[0] for p in points_bruts]
    tous_les_y = [p[1] for p in points_bruts]
    centre_x = (min(tous_les_x) + max(tous_les_x)) / 2
    centre_y = (min(tous_les_y) + max(tous_les_y)) / 2

    points_centres = []
    for x, y, stylo in points_bruts:
        points_centres.append((x - centre_x, y - centre_y, stylo))

    points_continus = []
    for i in range(len(points_centres)):
        x1, y1, stylo = points_centres[i]
        if stylo == 1 and i > 0:
            x0, y0, _ = points_centres[i-1]
            nb_segments = 50 
            for j in range(nb_segments + 1):
                nx = x0 + (j / nb_segments) * (x1 - x0)
                ny = y0 + (j / nb_segments) * (y1 - y0)
                points_continus.append((nx, ny))
        elif stylo == 1 and i == 0:
            points_continus.append((x1, y1))

    r_max_absolu = max([hypot(x, y) for x, y in points_continus]) if points_continus else 1
    matrice = [[None for _ in range(10)] for _ in range(360)]

    for x, y in points_continus:
        r = hypot(x, y)
        a = (degrees(atan2(y, x)) + 360) % 360
        angle_deg = int(a % 360)
        led = min(9, int((r / r_max_absolu) * 9))
        matrice[angle_deg][led] = (0, 255, 255)

    canvas.delete("all")
    angle = 0
    remanents = []

def animer():
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
    
    for pas in range(vitesse):
        angle = (angle + 1) % 360
        dernier_pas = (pas == vitesse - 1)
        
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
                    tid = canvas.create_oval(x-3, y-3, x+3, y+3, fill="cyan", outline="")
                    remanents.append({"id": tid, "vie": 255})
                    
    fenetre_h.after(20, animer)


def lancer(root):
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

    jauge_vitesse = ctk.CTkSlider(barre_bas, from_=1, to=20,
                                   command=changer_vitesse)
    jauge_vitesse.set(5)
    jauge_vitesse.pack(side="left", padx=10, fill="x", expand=True)

    animer()


if __name__ == "__main__":
    root = ctk.CTk()
    lancer(root)
    root.mainloop()