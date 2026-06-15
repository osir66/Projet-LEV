import customtkinter as ctk
import math
from lettres import LETTRES

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG = "#3a3a3a"
CANVAS_BG = "#111111"

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Semaphore LEV")
        self.root.configure(fg_color=BG)
        self.root.resizable(True, True)

        self.lettre_courante = 'A'
        self.grille = LETTRES[self.lettre_courante]
        self.nb_colonnes = len(self.grille[0])
        self.nb_lignes = len(self.grille)

        # barre du haut
        frame_top = ctk.CTkFrame(root, fg_color=BG)
        frame_top.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_top, text="Symbole",
                     text_color="#cccccc", font=("Arial", 11)).pack(side="left")

        self.entree = ctk.CTkEntry(frame_top, width=80,
                                   font=("Arial", 13, "bold"),
                                   fg_color="#4a4a4a", text_color="white",
                                   border_width=0, corner_radius=8)
        self.entree.insert(0, 'A')
        self.entree.pack(side="left", padx=10)

        ctk.CTkButton(frame_top, text="Afficher", width=90,
                      fg_color="#555555", hover_color="#666666",
                      text_color="white", font=("Arial", 11),
                      corner_radius=8,
                      command=self.changer_lettre).pack(side="left")

        self.label_lettre = ctk.CTkLabel(frame_top, text="A",
                                          text_color="#aaaaaa",
                                          font=("Arial", 11),
                                          fg_color=BG)
        self.label_lettre.pack(side="right")

        # canvas
        self.canvas_frame = ctk.CTkFrame(root, fg_color=CANVAS_BG, corner_radius=12)
        self.canvas_frame.pack(padx=20, pady=6)

        self.canvas = ctk.CTkCanvas(self.canvas_frame, width=540, height=540,
                                     bg=CANVAS_BG, highlightthickness=0, bd=0)
        self.canvas.pack(padx=8, pady=8)

        # barre du bas
        frame_bot = ctk.CTkFrame(root, fg_color=BG)
        frame_bot.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(frame_bot, text="Vitesse",
                     text_color="#cccccc", font=("Arial", 11)).pack(side="left")

        self.input_vitesse = ctk.CTkEntry(frame_bot, width=80,
                                           font=("Arial", 12),
                                           fg_color="#4a4a4a",
                                           text_color="white",
                                           border_width=0, corner_radius=8,
                                           placeholder_text="0.05")
        self.input_vitesse.pack(side="left", padx=10)
        self.input_vitesse.bind("<Return>", self.changer_vitesse_clavier)

        ctk.CTkLabel(frame_bot, text="entree pour valider",
                     text_color="#888888", font=("Arial", 10)).pack(side="left")

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
            self.label_lettre.configure(text=texte)
            self.dessiner()

    def changer_lettre_auto(self, forme, mission_name=""):
        if forme in LETTRES:
            self.lettre_courante = forme
            self.grille = LETTRES[forme]
            self.nb_colonnes = len(self.grille[0])
            self.nb_lignes = len(self.grille)
            if mission_name:
                self.label_lettre.configure(text=forme + "  " + mission_name)
            else:
                self.label_lettre.configure(text=forme)
            self.dessiner()

    # dessine la lettre au centre du canvas
    def dessiner(self):
        self.canvas.delete("all")
        taille = 25
        cx, cy = 270, 270
        ox = cx - self.nb_colonnes * taille // 2
        oy = cy - self.nb_lignes * taille // 2

        for li in range(self.nb_lignes):
            for co in range(self.nb_colonnes):
                led = self.grille[li][co]
                if led[0] == 1:
                    x = ox + co * taille + taille // 2
                    y = oy + li * taille + taille // 2
                    couleur = f'#{led[1]:02x}{led[2]:02x}{led[3]:02x}'
                    self.canvas.create_oval(x-7, y-7, x+7, y+7,
                                           fill=couleur, outline='')

    # boucle danimation
    def animer(self):
        self.dessiner()
        self.root.after(100, self.animer)