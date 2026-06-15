import customtkinter as ctk
import urllib.request
import threading
import time
from datetime import datetime, timezone
from lettres import LETTRES
from parseur import lire_json
import interface

# adresse du serveur a changer si lip change
SERVEUR = "http://192.168.1.22:8000"

CORRESPONDANCES = {
    "CERCLE": "ROND",
    "CIRCLE": "ROND",
    "SQUARE": "CARRE",
    "RECTANGLE": "CARRE",
    "HEART": "COEUR",
    "STAR": "ETOILE",
}

# variable pour eviter de traiter deux missions en meme temps
mission_active = None

# missions deja traitees pour eviter la boucle si le put echoue
missions_terminees = set()

# on recupere les donnees du serveur et on les lit avec notre parseur
def get_json(route):
    try:
        with urllib.request.urlopen(f"{SERVEUR}{route}", timeout=5) as r:
            return lire_json(r.read().decode())
    except:
        return None

# on envoie un put sans body
def put(route):
    try:
        req = urllib.request.Request(f"{SERVEUR}{route}", method='PUT')
        req.add_header("Content-Length", "0")
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

# on donne lheure actuelle au format du serveur
def maintenant():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f000Z")

# on traite une mission dans un thread separe
def traiter_mission(m, forme):
    global mission_active
    duree = int(m["time"]) if m["time"] else 10

    # on met le semaphore en occupied
    if m["semaphore_id"]:
        put("/api/update_semaphore/" + m["semaphore_id"] + "?state=Occupied")

    # on affiche la forme
    root.after(0, interface.vider)

    # on attend la duree
    time.sleep(duree)

    # on termine la mission et on enregistre lheure de fin
    fin = maintenant()
    put("/api/update_mission/" + m["id"] + "?state=Done&end_date=" + fin)

    # on remet le semaphore en available
    if m["semaphore_id"]:
        put("/api/update_semaphore/" + m["semaphore_id"] + "?state=Available")

    # on ajoute dans les terminees meme si le put a echoue
    missions_terminees.add(m["id"])

    # on vide laffichage
    root.after(0, lambda: interface.changer_lettre_auto(""))

    # on libere le verrou
    mission_active = None

def surveiller_serveur():
    global mission_active

    if mission_active is None:
        shapes = get_json("/api/list_shapes")
        missions = get_json("/api/list_missions")

        if shapes and missions:
            shapes_dict = {s["id"]: s["name"].strip().upper() for s in shapes}

            for m in missions:
                # on skip les missions deja traitees
                if m["id"] in missions_terminees:
                    continue

                etat = m["state"].strip().lower()

                if etat == "pending_semaphore" and m["shapes_id"] in shapes_dict:
                    forme = shapes_dict[m["shapes_id"]]
                    forme = CORRESPONDANCES.get(forme, forme)

                    if forme in LETTRES:
                        mission_active = m["id"]
                        t = threading.Thread(target=traiter_mission, args=(m, forme))
                        t.daemon = True
                        t.start()
                        break

    threading.Timer(2, surveiller_serveur).start()

# on cree la fenetre et on lance l interface
root = ctk.CTk()
interface.lancer(root)

threading.Timer(0, surveiller_serveur).start()

root.mainloop()