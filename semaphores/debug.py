import urllib.request
import urllib.parse
import json
import os

SERVEUR = "http://192.168.1.101:8000"

def get_json(route):
    with urllib.request.urlopen(f"{SERVEUR}{route}") as r:
        return json.loads(r.read())

def put(route):
    req = urllib.request.Request(f"{SERVEUR}{route}", data=b" ", method='PUT')
    try:
        urllib.request.urlopen(req)
    except:
        pass

def afficher_missions():
    missions = get_json("/api/list_missions")
    shapes = get_json("/api/list_shapes")
    shapes_dict = {s["id"]: s["name"].strip() for s in shapes}
    print("\n── MISSIONS ──────────────────────────────")
    for i, m in enumerate(missions):
        forme = shapes_dict.get(m["shapes_id"], "?") if m["shapes_id"] else "?"
        print(f"[{i+1}] {m['state']:15} | {m['name']:15} | forme: {forme}")
    print("──────────────────────────────────────────")
    return missions, shapes_dict

def main():
    while True:
        os.system('cls')
        missions, shapes_dict = afficher_missions()
        print("\n[A] Afficher une mission")
        print("[T] Terminer une mission")
        print("[Q] Quitter")
        choix = input("\n> ").strip().upper()

        if choix == "Q":
            break

        elif choix == "A":
            num = input("Numéro : ").strip()
            try:
                m = missions[int(num) - 1]
                put(f"/api/update_mission/{m['id']}?state=En Cours")
                print(f"✅ Mission passée En Cours")
            except Exception as e:
                print(f"❌ Erreur : {e}")
            input("Entrée pour continuer...")

        elif choix == "T":
            num = input("Numéro : ").strip()
            try:
                m = missions[int(num) - 1]
                put(f"/api/update_mission/{m['id']}?state=Terminee")
                print(f"✅ Mission terminée")
            except Exception as e:
                print(f"❌ Erreur : {e}")
            input("Entrée pour continuer...")

if __name__ == "__main__":
    main()