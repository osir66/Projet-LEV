import db
import base_projet
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

app.mount("/front", StaticFiles(directory="front"), name="front")

#------------------------------ Routes de la page d'accueil ----------------------------------

# Route pour la page d’accueil
@app.get("/commande", tags=["Interface"])
def page_html():
    return FileResponse("index.html")
@app.get("/", tags=["Interface"])
def redirect_to_commande():
    stats = db.getStatistique()
    with open("stat.html", "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("__COUNT_ROBOTS__",     str(stats["robots"]))
    html = html.replace("__COUNT_SEMAPHORES__", str(stats["semaphores"]))
    html = html.replace("__COUNT_FORMES__",     str(stats["formes"]))
    html = html.replace("__COUNT_MISSIONS__",   str(stats["missions"]))
    return HTMLResponse(content=html)

@app.get("/mattieux", tags=["Interface"])
def mattieux_page():
   with open("airbus.html", "r", encoding="utf-8") as f:    
    html = f.read()
    html = html.replace("__COUNT_ROBOTS__",     str(db.count_robots()))
    html = html.replace("__COUNT_SEMAPHORES__", str(db.count_semaphores()))
    html = html.replace("__COUNT_FORMES__",     str(db.count_formes()))
    html = html.replace("__COUNT_MISSIONS__",   str(db.count_missions()))
    return HTMLResponse(content=html)

#-----------------------------------------------------------------------------------

#------------------------------ Routes des Sémaphores ----------------------------------

#route pour lister les sémaphores
@app.get("/api/list_semaphore", tags=["Sémaphores"])
def list_semaphore():
    return db.list_semaphore()

#route pour liste le sémaphore en fonction de son id 
@app.get("/api/semaphore/{id}", tags=["Sémaphores"])
def get_semaphore(id: str):
    return db.get_semaphore(id)

#route pour ajouter un sémaphore
@app.post("/api/add_semaphore", tags=["Sémaphores"])
def add_semaphore(name: str = Form(...),type: str= Form(...),coord_x : int= Form(...),coord_y:int= Form(...)):
    return db.add_semaphore(name, type,coord_x,coord_y)

#route pour modifier un sémaphore en fonction de l'id
@app.put("/api/update_semaphore/{id}", tags=["Sémaphores"])
def update_semaphore(id: str, name: str | None = None, state: str | None = None,
                            type: str | None = None,
                           coord_x : int| None = None,
                           coord_y : int | None = None):
    return db.update_semaphore(id, name, state, type,coord_x,coord_y)

#-----------------------------------------------------------------------------------

#------------------------------ Routes des Robots ----------------------------------

#route pour lister les robots 
@app.get("/api/list_robots", tags=["Robots"])
def list_robots():
    return db.list_robots()

#route pour lister le robot en fonction de l'id
@app.get("/api/robot/{id}", tags=["Robots"])
def get_robot(id: str):
    return db.get_robot(id)

#route pour récupérer une mission pour un robot 
@app.get("/robot/{id}/mission", tags=["Robots"])
def get_robot_mission(id: str):
    return db.get_robot_mission(id)

#route pour ajouter un robot
@app.post("/api/add_robot", tags=["Robots"])
def add_robot(name: str | None = Form(None), speed: float | None = Form(None),position_x: float | None = Form(None), position_y: int | None = Form(None)):
    return db.add_robot(name,"Available", speed, position_x, position_y)

#route pour modifier un robot en fonction de l'id
@app.put("/api/update_robot/{id}", tags=["Robots"])
def update_robot(id: str, name: str | None = None, state: str | None = None, speed: int | None = None, 
                position_x: float | None = None, position_y: float | None = None):
    return db.update_robot(id, name, state, speed, position_x, position_y)

#-----------------------------------------------------------------------------------


#------------------------------ Routes des Missions --------------------------------

#route pour afficher les missions d'un équipe 
@app.get("/api/list_missions_by_team", tags=["Missions"])
def get_missions(team : str =""):
    return db.get_mission(team)

#route pour lister les missions 
@app.get("/api/list_missions", tags=["Missions"])
def list_missions():
    return db.list_missions()

#route pour ajouter une mission 
@app.post("/api/add_mission", tags=["Missions"])
def add_mission(name : str | None = None, semaphore_id : str| None = None , robot_id : str | None = None, shape_id: str | None = None , team_id : str | None = None ,state : str ="Awaiting",
                start_date : str ="", end_date : str = "",team : str ="", time : int = ""):    
    return db.ajouter_mission(name, semaphore_id, robot_id,shape_id, team_id,state, start_date, end_date,team, time)
 
#route pour modifier une mission en fonction de l'id
@app.put("/api/update_mission/{id}", tags=["Missions"])
def update_mission(id: str, name: str | None = None, semaphore_id: str | None = None,
                         robot_id: str | None = None, shape_id: str | None = None,
                         state: str | None = None, start_date: str | None = None,
                         end_date: str | None = None, team: str | None = None,
                         time: str | None = None):
    return db.modifier_mission(id,name,semaphore_id,robot_id,shape_id,state,start_date,end_date,team,time)

#-----------------------------------------------------------------------------------


#------------------------------ Routes des Équipes ---------------------------------

#route pour lister les équipes 
@app.get("/api/list_teams", tags=["Équipes"])
def list_equipes():
    return db.list_equipes()

#route pour ajouter une équipe 
@app.post("/api/add_team", tags=["Équipes"])
def add_team(name: str, ip: str | None = None, allowed: bool = False):
    return db.ajouter_equipe(name, ip, allowed)

#route pour modifier une équipe en fonction de l'id
@app.put("/api/update_team/{id}", tags = ["Équipes"])
def put_team(id: str, name: str | None = None, ip: str | None = None,
            allowed: bool | None = None):
    return db.modifier_equipe(id,name,ip,allowed)


#-----------------------------------------------------------------------------------

#------------------------------ Routes des Formes ---------------------------------

#route pour lister les formes 
@app.get("/api/list_shapes", tags=["Formes"])
def list_formes():
    return db.list_formes()

#route pour afficher la forme en fonction de son id 
@app.get("/api/shape/{id}", tags=["Formes"])
def get_shape(id: str):
    return db.get_shape(id)

#route pour ajouter une forme 
@app.post("/api/add_shape", tags=["Formes"])
def add_shape(name: str = Form(...),image: str = Form(...)):
    return db.ajouter_forme(name,image)

#route pour modifier une forme en fonction de l'id
@app.put("/update_shape/{id}", tags = ["Formes"])
def update_shape (id: str, name: str | None = None, image: str | None = None):
    return db.update_shape(id,name,image)

#route pour trouver le fichier csv dans le fichier "fish"
@app.post("/api/import_shape_csv", tags=["Formes"])
async def import_shape_csv(file: UploadFile = File(...)):
    
    #chemin ou le fichier sera enregistré 
    c = Path(__file__).resolve().parent.parent / "fish" / file.filename
    
    #lis le fichier et l'enregistre 
    fichier_contenu = await file.read()
    c.write_bytes(fichier_contenu)
    
    db.import_csv(str(c))
    return RedirectResponse(url="/commande", status_code=303)

#-----------------------------------------------------------------------------------

#------------------------------ Routes configuration ---------------------------------

#route pour afficher la configuration des grilles 
@app.get("/api/get_config", tags = ["Configuration"])
def get_config():
    return db.get_config()

# route pour ajouter une configuration de grille 
@app.post("/api/add_config", tags=["Configuration"])
def add_config(grille: str = Form(...), nbr_semaphore: int = Form(...), nbr_robot: int = Form(...), 
            nb_x: float = Form(...), nb_y: float = Form(...)):
    return db.add_config(grille, nbr_semaphore, nbr_robot, nb_x, nb_y)

# Route pour créer une grille et ses segments
@app.post("/api/creer_grille", tags=["Configuration"])
def creer_grille(name: str = Form(...)):
    return db.faire_grille(name)

#route pour afficher les segments 
@app.get("/api/list_segment", tags=["Configuration"])
def recup_segments():
    return db.afficher_seg()

#-----------------------------------------------------------------------------------

#------------------------------ Route Healthcheck ---------------------------------
#route pour vérifier la connexion 
@app.get("/api/health", tags=["Health"])
def healthcheck():
    return db.healthcheck()

#-----------------------------------------------------------------------------------



