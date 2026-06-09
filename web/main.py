import db
import base_projet
from fastapi import FastAPI
import datetime

app = FastAPI()

#@app.get("/)")
#def page_html():
    #return "<h1>Bienvenue sur l'API Massilia</h1>"

#------------------------------ Routes des Sémaphores ----------------------------------

@app.get("/api/list_semaphore", tags=["Sémaphores"])
def list_semaphore():
    return db.list_semaphore()


@app.get("/api/semaphore/{id}", tags=["Sémaphores"])
def get_semaphore(id: str):
    return db.get_semaphore(id)


@app.post("/api/add_semaphore", tags=["Sémaphores"])
def add_semaphore(name: str, duration: int, type: str,coord_x : int,coord_y:int):
    return db.add_semaphore(name, duration, type,coord_x,coord_y)


@app.put("/api/update_semaphore/{id}", tags=["Sémaphores"])
def update_semaphore(id: str, name: str | None = None, state: str | None = None,
                           duration: int | None = None, type: str | None = None,
                           coord_x : int| None = None,
                           coord_y : int | None = None):
    return db.update_semaphore(id, name, duration, state, type,coord_x,coord_y)

#-----------------------------------------------------------------------------------

#------------------------------ Routes des Robots ----------------------------------

@app.get("/api/list_robots", tags=["Robots"])
def list_robots():
    return db.list_robots()

@app.get("/api/robot/{id}", tags=["Robots"])
def get_robot(id: str):
    return db.get_robot(id)

@app.get("/robot/{id}/mission", tags=["Robots"])
def get_robot_mission(id: str):
    return db.get_robot_mission(id)

@app.post("/api/add_robot", tags=["Robots"])
def add_robot(name: str | None = None, speed: int | None = None,position_x: int | None = None, position_y: int | None = None):
    return db.add_robot(name,"en cours", speed, position_x, position_y)

@app.put("/api/update_robot/{id}", tags=["Robots"])
def update_robot(id: str, name: str | None = None, state: str | None = None, speed: int | None = None, 
                position_x: int | None = None, position_y: int | None = None):
    return db.update_robot(id, name, state, speed, position_x, position_y)

#-----------------------------------------------------------------------------------


#------------------------------ Routes des Missions --------------------------------

@app.get("/api/get_missions", tags=["Missions"])
def get_missions(team : str):
    return db.get_mission(team)

@app.get("/api/list_missions", tags=["Missions"])
def list_missions():
    return db.list_missions()

@app.post("/api/add_mission", tags=["Missions"])
def add_mission(name : str | None = None, semaphore_id : str| None = None , robot_id : str | None = None, shape_id: str | None = None , team_id : str | None = None ,state : str ="En attente",
                start_date : str ="", end_date : str = "",team : str ="", time : int = ""):    
    return db.ajouter_mission(name, semaphore_id, robot_id,shape_id, team_id,state, start_date, end_date,team, time)
 
@app.put("/api/update_mission/{id}", tags=["Missions"])
def update_mission(id: str, name: str | None = None, semaphore_id: str | None = None,
                         robot_id: str | None = None, shape_id: str | None = None,
                         state: str | None = None, start_date: str | None = None,
                         end_date: str | None = None, team: str | None = None,
                         time: str | None = None):
    return db.modifier_mission(id,name,semaphore_id,robot_id,shape_id,state,start_date,end_date,team,time)

#-----------------------------------------------------------------------------------


#------------------------------ Routes des Équipes ---------------------------------

@app.get("/api/list_teams", tags=["Équipes"])
def list_equipes():
    return db.list_equipes()

@app.post("/api/add_team", tags=["Équipes"])
def add_team(name: str, ip: str | None = None, allowed: bool = False):
    return db.ajouter_equipe(name, ip, allowed)

@app.put("/api/update_team/{id}", tags = ["Équipes"])
def put_team(id: str, name: str | None = None, ip: str | None = None,
            allowed: bool | None = None):
    return db.modifier_equipe(id,name,ip,allowed)


#-----------------------------------------------------------------------------------

#------------------------------ Routes des Formes ---------------------------------

@app.get("/api/list_shapes", tags=["Formes"])
def list_formes():
    return db.list_formes()

@app.post("/api/shapes/{id}", tags=["Formes"])
def get_shape(id: str):
    return db.get_shape(id)

@app.post("/api/add_shape", tags=["Formes"])
def add_shape(name: str, image: str):
    return db.ajouter_forme(name, image)

@app.put("/update_shape/{id}", tags = ["Formes"])
def update_shape (id: str, name: str | None = None, image: str | None = None):
    return db.update_shape(id,name,image)

#-----------------------------------------------------------------------------------

#------------------------------ Routes configuration ---------------------------------


@app.get("/api/get_config", tags = ["Configuration"])
def get_config():
    return db.get_config()

@app.post("/api/add_config", tags = ["Configuration"])
def add_config(grille : str ,nbr_semaphore : int ,nbr_robot : int):
    return db.add_config(grille,nbr_semaphore,nbr_robot)

@app.put("/api/update_config", tags = ["Configuration"])
def put_config(grille : str | None = None,nbr_semaphore : int| None = None ,nbr_robot : int| None = None):
    return db.update_config(grille,nbr_semaphore,nbr_robot)