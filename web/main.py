import db, base_projet
from fastapi import FastAPI

app = FastAPI()

@app.get("/afficher_semaphore")
def afficher_semaphore():
    return db.afficher_semaphore()

@app.post("/ajouter_semaphore")
def ajouter_semaphore(id: str, etat: bool, dessin_forme: str, matrice: float):
    return db.ajouter_semaphore(id, etat, dessin_forme, matrice)

@app.post("/supprimer_semaphore")
def supprimer_semaphore(id: str):
    return db.supprimer_semaphore(id)

@app.post("/modifier_semaphore")
def modifier_semaphore(id : str, etat: bool, dessin_forme: str, matrice: float):
    return db.modifier_semaphore(id,etat, dessin_forme, matrice)

@app.post("/ajouter_robot")
def ajouter_robot(id: str, position_actuelle_x: float, position_actuelle_y: float, est_disponible: bool, vitesse_deplacement: float):
    return db.ajouter_robot(id, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement)

@app.post("/suprimer_robot")
def suprimer_robot(id : str):
    return db.supprimer_robot(id) 