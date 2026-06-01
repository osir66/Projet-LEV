from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def lire_racine():
    return {"message": "Bienvenue sur mon serveur FastAPI !"}


