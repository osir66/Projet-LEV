import db
import base_projet
from fastapi import FastAPI
import datetime

app = FastAPI()

@app.get("/afficher_semaphore")
def afficher_semaphore():
    return db.afficher_semaphore()

@app.post("/ajouter_semaphore")
def ajouter_semaphore( etat: bool, dessin_forme: str, matrice: float):
    return db.ajouter_semaphore( etat, dessin_forme, matrice)

@app.delete("/supprimer_semaphore")
def supprimer_semaphore(id: str):
    return db.supprimer_semaphore(id)

@app.post("/modifier_semaphore")
def modifier_semaphore(id : str, etat: bool, dessin_forme: str, matrice: float):
    return db.modifier_semaphore(id,etat, dessin_forme, matrice)

@app.post("/ajouter_robot")
def ajouter_robot(nom_robot: str, position_actuelle_x: float, position_actuelle_y: float, est_disponible: bool, vitesse_deplacement: float):
    return db.ajouter_robot(nom_robot, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement)

@app.delete("/suprimer_robot")
def suprimer_robot(id : str):
    return db.supprimer_robot(id) 

@app.get("/afficher_robot")
def afficher_robot():
    return db.afficher_robot()

@app.post("/ajouter_equipe")
def ajouter_equipe(nom_equipe: str, ip_equipe: str):
    return db.ajouter_equipe(nom_equipe, ip_equipe)

@app.post("/ajouter_forme")
def ajouter_forme(type_forme: str):
    return db.ajouter_forme(type_forme)

@app.get("/afficher_forme")
def afficher_forme():
    return db.afficher_forme()

@app.post("/ajouter_mission")
def ajouter_mission(id_semaphore : str, id_forme : str, id_robot : str, status : str, heure_exec : datetime.datetime):
    return db.ajouter_mission(id_semaphore, id_forme, id_robot, status, heure_exec)

