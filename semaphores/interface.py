import customtkinter as ctk
import math
from lettres import LETTRES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG = "#0d0d0d"
BRANCH_COLOR = "#2a2a2a"
LED_OFF = "#1a1a1a"

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Sémaphore LEV")
        self.root.configure(fg_color=BG)
        self.root.resizable(True, True)
        self.angle = 0
        self.vitesse = 0.05
        self.lettre_courante = 'A'
        self.grille = LETTRES[self.lettre_courante]
        self.nb_colonnes = len(self.grille[0])
        self.nb_lignes = len(self.grille)

        # Barre du haut
        frame_top = ctk.CTkFrame(root, fg_color=BG)
        frame_top.pack(fill="x", padx=20, pady=12)

        ctk.CTkLabel(frame_top, text="Symbole", text_color="#888888",
                     font=("Arial", 11)).pack(side="left")

        self.entree = ctk.CTkEntry(frame_top, width=80, font=("Arial", 13, "bold"),
                                   fg_color="#1c1c1c", text_color="white",
                                   border_width=0, corner_radius=8)
        self.entree.insert(0, 'A')
        self.entree.pack(side="left", padx=10)

        ctk.CTkButton(frame_top, text="Afficher", width=90,
                      fg_color="#2a2a2a", hover_color="#3a3a3a",
                      text_color="white", font=("Arial", 11),
                      corner_radius=8, command=self.changer_lettre).pack(side="left")

        self.label_lettre = ctk.CTkLabel(frame_top, text="● A",
                                          text_color="#555555", font=("Arial", 11),
                                          fg_color=BG)
        self.label_lettre.pack(side="right")

        # Canvas
        self.canvas_frame = ctk.CTkFrame(root, fg_color="#111111", corner_radius=16)
        self.canvas_frame.pack(padx=20, pady=4)

        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=560, height=560,
                                     bg="#111111", highlightthickness=0, bd=0)
        self.canvas.pack(padx=10, pady=10)

        # Vitesse
        frame_bot = ctk.CTkFrame(root, fg_color=BG)
        frame_bot.pack(fill="x", padx=20, pady=12)

        ctk.CTkLabel(frame_bot, text="Vitesse", text_color="#888888",
                     font=("Arial", 11)).pack(side="left")

        self.input_vitesse = ctk.CTkEntry(frame_bot, width=80, font=("Arial", 12),
                                           fg_color="#1c1c1c", text_color="white",
                                           border_width=0, corner_radius=8,
                                           placeholder_text="0.05")
        self.input_vitesse.pack(side="left", padx=10)
        self.input_vitesse.bind("<Return>", self.changer_vitesse_clavier)

        ctk.CTkLabel(frame_bot, text="→ Entrée pour valider",
                     text_color="#444444", font=("Arial", 10)).pack(side="left")

        self.animer()

    def changer_vitesse_clavier(self, event):
        try:
            val = float(self.input_vitesse.get())
            if 0 <= val <= 1000:
                self.vitesse = val
        except:
            pass

    def changer_lettre(self):
        texte = self.entree.get().upper()
        if texte in LETTRES:
            self.lettre_courante = texte
            self.grille = LETTRES[texte]
            self.nb_colonnes = len(self.grille[0])
            self.nb_lignes = len(self.grille)
            self.label_lettre.configure(text=f"● {texte}")
            self.canvas.delete("all")

    def changer_lettre_auto(self, forme, mission_name=""):
        if forme in LETTRES:
            self.lettre_courante = forme
            self.grille = LETTRES[forme]
            self.nb_colonnes = len(self.grille[0])
            self.nb_lignes = len(self.grille)
            if mission_name:
                self.label_lettre.configure(text=f"● {forme}  ({mission_name})")
            else:
                self.label_lettre.configure(text=f"● {forme}")
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
                    self.canvas.create_oval(x-7, y-7, x+7, y+7,
                                           fill=couleur, outline='')

    def dessiner_branches(self, cx, cy):
        longueur = 260
        for i in range(4):
            angle = self.angle + i * (math.pi / 2)
            x_bout = cx + longueur * math.cos(angle)
            y_bout = cy + longueur * math.sin(angle)
            self.canvas.create_line(cx, cy, x_bout, y_bout,
                                    fill=BRANCH_COLOR, width=2)

            for j in range(self.nb_lignes):
                rx = cx + (j + 1) * 24 * math.cos(angle)
                ry = cy + (j + 1) * 24 * math.sin(angle)

                col_idx = int((self.angle % (2 * math.pi)) / (2 * math.pi) * self.nb_colonnes)
                col_idx = col_idx % self.nb_colonnes
                led = self.grille[j][col_idx]

                if led[0] == 1:
                    couleur = f'#{led[1]:02x}{led[2]:02x}{led[3]:02x}'
                    self.canvas.create_oval(rx-5, ry-5, rx+5, ry+5,
                                           fill=couleur, outline='')
                else:
                    self.canvas.create_oval(rx-3, ry-3, rx+3, ry+3,
                                           fill=LED_OFF, outline='')

    def animer(self):
        self.canvas.delete("all")
        cx, cy = 280, 280
        self.dessiner_lettre(cx, cy)
        self.dessiner_branches(cx, cy)
        self.angle += self.vitesse
        delai = max(1, int(16 / (1 + self.vitesse * 0.1)))
        self.root.after(delai, self.animer)