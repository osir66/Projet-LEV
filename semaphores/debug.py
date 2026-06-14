import urllib.request
import time
from datetime import datetime, timezone
from parseur import lire_json

SERVEUR = "http://192.168.1.22:8000"

# dictionnaire pour traduire les noms du serveur vers les noms de lettres.py
CORRESPONDANCES = {
    "CERCLE": "ROND",
    "CIRCLE": "ROND",
    "SQUARE": "CARRE",
    "RECTANGLE": "CARRE",
    "HEART": "COEUR",
    "STAR": "ETOILE",
}

# on appelle le serveur et on lit le resultat avec notre parseur
def get_json(route):
    with urllib.request.urlopen(f"{SERVEUR}{route}") as r:
        return lire_json(r.read().decode())

# on envoie un put au serveur pour modifier une donnee
def put(route):
    try:
        req = urllib.request.Request(f"{SERVEUR}{route}", method='PUT')
        req.add_header("Content-Length", "0")
        urllib.request.urlopen(req, timeout=2)
    except:
        pass

# on donne lheure actuelle au format du serveur
def maintenant():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f000Z")

# on recupere toutes les missions pending et on les affiche une par une
def lancer_missions():

    # on recupere les formes disponibles sur le serveur
    shapes = get_json("/api/list_shapes")
    shapes_dict = {s["id"]: s["name"].strip().upper() for s in shapes}

    # on recupere toutes les missions
    missions = get_json("/api/list_missions")

    # on garde seulement les missions en attente avec une forme valide
    missions_valides = []
    for m in missions:
        if m["state"].strip() in ["Pending", "En attente"] and m["shapes_id"] in shapes_dict:
            missions_valides.append(m)

    if not missions_valides:
        print("aucune mission")
        return

    # on boucle sur chaque mission valide
    for i, m in enumerate(missions_valides):

        # on recupere le nom de la forme et on traduit si besoin
        forme = shapes_dict[m["shapes_id"]]
        forme = CORRESPONDANCES.get(forme, forme)

        # on recupere la duree d affichage depuis la mission
        duree = int(m["time"]) if m["time"] else 10

        # on affiche les infos de la mission dans le terminal
        print(str(i+1) + " " + m["name"] + " " + forme + " " + str(duree) + "s")

        # on attend la duree demandee
        time.sleep(duree)

        # on dit au serveur que la mission est done avec lheure de fin
        fin = maintenant()
        put("/api/update_mission/" + m["id"] + "?state=Done&end_date=" + fin)
        print("Done")

    print("fin")

if __name__ == "__main__":
    lancer_missions()