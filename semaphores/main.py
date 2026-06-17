import customtkinter as ctk
import urllib.request
import threading
import time
from datetime import datetime
from parseur import lire_json

ip = input("IP du serveur (ex: 192.168.1.22) : ")
SERVEUR = "http://" + ip + ":8000"

mission_active = None
missions_terminees = set()

fenetre_symbole = None
fenetre_table = None
fenetre_helice = None


def get_json(route):
    """envoie une requete get au serveur et lit la reponse avec le parseur maison"""
    try:
        with urllib.request.urlopen(f"{SERVEUR}{route}", timeout=5) as r:
            return lire_json(r.read().decode())
    except:
        return None


def put(route):
    """envoie une requete put sans contenu au serveur pour changer un etat"""
    try:
        req = urllib.request.Request(f"{SERVEUR}{route}", method='PUT')
        req.add_header("Content-Length", "0")
        urllib.request.urlopen(req, timeout=5)
    except:
        pass


def maintenant():
    """donne l heure locale actuelle au format attendu par le serveur"""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f000Z")


def ouvrir_symbole(caractere, nom_mission):
    """ouvre la fenetre symbole si besoin puis affiche le caractere demande"""
    global fenetre_symbole
    import interface
    if fenetre_symbole is None or not fenetre_symbole.winfo_exists():
        fenetre_symbole = ctk.CTkToplevel(root)
        interface.lancer(fenetre_symbole)
    interface.changer_lettre_auto(caractere, nom_mission)


def ouvrir_table(image_shape):
    """ouvre la fenetre table tracante si besoin puis charge le csv recu"""
    global fenetre_table
    import table_tracante
    if fenetre_table is None or not fenetre_table.winfo_exists():
        fenetre_table = ctk.CTkToplevel(root)
        table_tracante.lancer(fenetre_table)
    if image_shape and image_shape not in ["test", ""]:
        fenetre_table.after(200, lambda: table_tracante.charger_depuis_texte(image_shape))


def ouvrir_helice(image_shape):
    """ouvre la fenetre helice si besoin puis charge le csv recu"""
    global fenetre_helice
    import helice as helice_module
    if fenetre_helice is None or not fenetre_helice.winfo_exists():
        fenetre_helice = ctk.CTkToplevel(root)
        helice_module.lancer(fenetre_helice)
    if image_shape and image_shape not in ["test", ""]:
        fenetre_helice.after(200, lambda: helice_module.charger_depuis_texte(image_shape))


def traiter_mission(m, type_sem, shape):
    """traite une mission du debut a la fin dans un thread separe
    ouvre la bonne fenetre attend la duree puis previent le serveur et ferme"""
    global mission_active, fenetre_symbole, fenetre_table, fenetre_helice
    duree = int(m["time"]) if m["time"] else 10

    image_shape = shape["image"].strip() if shape["image"] else ""
    nom_shape = shape["name"].strip()

    if len(image_shape) == 1:
        caractere = image_shape
    else:
        caractere = nom_shape[0] if len(nom_shape) > 0 else "?"

    type_sem = type_sem.lower()

    if m["semaphore_id"]:
        put("/api/update_semaphore/" + m["semaphore_id"] + "?state=Occupied")

    if type_sem in ["symbole", "ascii"]:
        root.after(0, lambda c=caractere, n=m["name"]: ouvrir_symbole(c, n))
    elif type_sem in ["table", "tracant"]:
        root.after(0, lambda i=image_shape: ouvrir_table(i))
    elif type_sem == "helice":
        root.after(0, lambda i=image_shape: ouvrir_helice(i))

    time.sleep(duree)

    fin = maintenant()
    put("/api/update_mission/" + m["id"] + "?state=Done&end_date=" + fin)

    if m["semaphore_id"]:
        put("/api/update_semaphore/" + m["semaphore_id"] + "?state=Available")

    missions_terminees.add(m["id"])

    try:
        if type_sem in ["symbole", "ascii"] and fenetre_symbole and fenetre_symbole.winfo_exists():
            root.after(0, fenetre_symbole.destroy)
            fenetre_symbole = None
        elif type_sem in ["table", "tracant"] and fenetre_table and fenetre_table.winfo_exists():
            root.after(0, fenetre_table.destroy)
            fenetre_table = None
        elif type_sem == "helice" and fenetre_helice and fenetre_helice.winfo_exists():
            root.after(0, fenetre_helice.destroy)
            fenetre_helice = None
    except:
        pass

    mission_active = None


def surveiller_serveur():
    """boucle qui tourne toutes les 2 secondes et cherche une mission en attente
    si elle en trouve une elle la lance dans un nouveau thread"""
    global mission_active

    if mission_active is None:
        shapes = get_json("/api/list_shapes")
        missions = get_json("/api/list_missions")
        semaphores = get_json("/api/list_semaphore")

        if shapes and missions and semaphores:
            shapes_dict = {s["id"]: s for s in shapes}
            semaphores_dict = {s["id"]: s for s in semaphores}

            for m in missions:
                if m["id"] in missions_terminees:
                    continue

                etat = m["state"].strip().lower()

                shape_id = m.get("shapes_id") or m.get("shape_id")

                if etat == "pending_semaphore":
                    if shape_id and shape_id in shapes_dict:
                        shape = shapes_dict[shape_id]
                        sem_id = m["semaphore_id"]

                        if sem_id in semaphores_dict:
                            type_sem = semaphores_dict[sem_id]["type"]
                        else:
                            type_sem = "symbole"

                        mission_active = m["id"]
                        t = threading.Thread(target=traiter_mission,
                                            args=(m, type_sem, shape))
                        t.daemon = True
                        t.start()
                        break
                    else:
                        print("erreur la mission " + m["name"] + " utilise une shape introuvable")

    threading.Timer(2, surveiller_serveur).start()


root = ctk.CTk()
root.withdraw()

threading.Timer(0, surveiller_serveur).start()

root.mainloop()

# main.py — le cerveau. Il demande l'IP, surveille le serveur en boucle (surveiller_serveur),
# et quand une mission arrive il décide quoi faire (traiter_mission) et ouvre la bonne fenêtre 
# (ouvrir_symbole, ouvrir_table, ouvrir_helice). C'est le seul fichier qui parle au serveur 
# via get_json et put.