import db, base_projet
from fastapi import FastAPI

app = FastAPI()

@app.get("/afficher_semaphore")
def afficher_semaphore():
    return db.afficher_semaphore()

@app.post("/ajouter_semaphore")
def ajouter_semaphore(id: str, etat: bool, dessin_forme: str, matrice: float):
    return db.ajouter_semaphore(id, etat, dessin_forme, matrice)


