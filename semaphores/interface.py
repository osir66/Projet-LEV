# Interface demo 

import tkinter as tk
import math
from lettres import LETTRES

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Sémaphore LEV")
        self.angle = 0
        self.vitesse = 0.05
        self.lettre_courante = 'A'
        self.grille = LETTRES[self.lettre_courante]
        self.nb_colonnes = len(self.grille[0])
        self.nb_lignes = len(self.grille)

        frame_top = tk.Frame(root, bg='black')
        frame_top.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(frame_top, text="Lettre/Symbole :", fg='white', bg='black').pack(side=tk.LEFT)
        self.entree = tk.Entry(frame_top, width=10)
        self.entree.insert(0, 'A')
        self.entree.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Afficher", command=self.changer_lettre).pack(side=tk.LEFT)

        self.slider = tk.Scale(root, from_=0.01, to=0.5, resolution=0.01,
                               orient=tk.HORIZONTAL, label="Vitesse",
                               fg='white', bg='black',
                               command=self.changer_vitesse)
        self.slider.set(self.vitesse)
        self.slider.pack(fill=tk.X, padx=10)

        self.canvas = tk.Canvas(root, width=600, height=600, bg='black')
        self.canvas.pack()

        self.animer()

    def changer_vitesse(self, val):
        self.vitesse = float(val)

    def changer_lettre(self):
        texte = self.entree.get().upper()
        if texte in LETTRES:
            self.lettre_courante = texte
            self.grille = LETTRES[texte]
            self.nb_colonnes = len(self.grille[0])
            self.nb_lignes = len(self.grille)
            self.canvas.delete("all")

    def dessiner_lettre(self, cx, cy):
        taille_case = 25
        largeur_lettre = self.nb_colonnes * taille_case
        hauteur_lettre = self.nb_lignes * taille_case
        offset_x = cx - largeur_lettre // 2
        offset_y = cy - hauteur_lettre // 2

        for ligne_idx in range(self.nb_lignes):
            for col_idx in range(self.nb_colonnes):
                led = self.grille[ligne_idx][col_idx]
                if led[0] == 1:
                    x = offset_x + col_idx * taille_case + taille_case // 2
                    y = offset_y + ligne_idx * taille_case + taille_case // 2
                    couleur = f'#{led[1]:02x}{led[2]:02x}{led[3]:02x}'
                    self.canvas.create_oval(x-6, y-6, x+6, y+6, fill=couleur, outline='')

    def dessiner_branches(self, cx, cy):
        longueur = 280
        for i in range(4):
            angle = self.angle + i * (math.pi / 2)
            x_bout = cx + longueur * math.cos(angle)
            y_bout = cy + longueur * math.sin(angle)
            self.canvas.create_line(cx, cy, x_bout, y_bout, fill='gray40', width=2)

            for j in range(self.nb_lignes):
                rx = cx + (j + 1) * 25 * math.cos(angle)
                ry = cy + (j + 1) * 25 * math.sin(angle)

                col_idx = int((self.angle % (2 * math.pi)) / (2 * math.pi) * self.nb_colonnes)
                col_idx = col_idx % self.nb_colonnes
                led = self.grille[j][col_idx]

                if led[0] == 1:
                    couleur = f'#{led[1]:02x}{led[2]:02x}{led[3]:02x}'
                else:
                    couleur = 'gray20'

                self.canvas.create_oval(rx-4, ry-4, rx+4, ry+4, fill=couleur, outline='')

    def animer(self):
        self.canvas.delete("all")
        cx, cy = 300, 300
        self.dessiner_lettre(cx, cy)
        self.dessiner_branches(cx, cy)
        self.angle += self.vitesse
        self.root.after(16, self.animer)

root = tk.Tk()
app = Interface(root)
root.mainloop()