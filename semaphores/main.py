import customtkinter as ctk
import urllib.request
import json
from interface import Interface

SERVEUR = "http://192.168.1.101:8000"

CORRESPONDANCES = {
    "CERCLE": "ROND",
    "CIRCLE": "ROND",
    "SQUARE": "CARRE",
    "RECTANGLE": "CARRE",
    "HEART": "COEUR",
    "STAR": "ETOILE",
}

def get_json(route):
    with urllib.request.urlopen(f"{SERVEUR}{route}") as r:
        return json.loads(r.read())

def surveiller_serveur():
    try:
        shapes = get_json("/api/list_shapes")
        shapes_dict = {s["id"]: s["name"].strip().upper() for s in shapes}

        missions = get_json("/api/list_missions")
        mission_trouvee = None
        for m in missions:
            if m["state"].strip() in ["En Cours", "En cours", "In Progress", "Pending"] and m["shapes_id"] in shapes_dict:
                mission_trouvee = m
                break

        if mission_trouvee:
            forme = shapes_dict[mission_trouvee["shapes_id"]]
            forme = CORRESPONDANCES.get(forme, forme)
            if forme in ["A", "B", "C", "CARRE", "ROND", "COEUR", "ETOILE", "TRIANGLE"]:
                app.changer_lettre_auto(forme, mission_trouvee["name"])
        else:
            app.changer_lettre_auto("A")

    except:
        pass
    root.after(2000, surveiller_serveur)

root = ctk.CTk()
root.geometry("700x620")
root.resizable(True, True)
app = Interface(root)

surveiller_serveur()
root.mainloop()