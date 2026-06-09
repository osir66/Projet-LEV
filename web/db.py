import base_projet
import sqlite3
from sqlite3 import Error
import uuid

#------------------------------ Fonctions des Sémaphores ----------------------------------
def list_semaphore():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SEMAPHORES''')
        afficher_semaphore = [dict(row) for row in c.fetchall()]
        print (afficher_semaphore)
        return afficher_semaphore
    except Error as e:
        print("Error:",e)
        return "Erreur de l'affichage des semaphores", e
    finally:
        conn.commit()
        conn.close()
        


def get_semaphore(id):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SEMAPHORES WHERE id = ?''', (id,))
        afficher_semaphore = [dict(row) for row in c.fetchall()]
        return afficher_semaphore
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage du semaphore","de l'id :",id, e
    finally:
        conn.commit()
        conn.close()


def add_semaphore(nom, duration, type,coord_x,coord_y):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, nom, duration, type,coord_x,coord_y)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO SEMAPHORES (id,name,duration,type,coord_x,coord_y) VALUES (?, ?, ?, ?,?,?)''',
              (nouvel_uuid, nom, duration, type,coord_x,coord_y))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout du semaphore", e
    conn.commit()
    conn.close()
    return "Semaphore ajouté avec succès"


def update_semaphore(id, nom, duration, state, type,coord_x,coord_y):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    
    champs = []
    valeurs = []
    
    if nom is not None: champs.append("name = ?"); valeurs.append(nom)
    if duration is not None: champs.append("duration = ?"); valeurs.append(duration)
    if state is not None: champs.append("state = ?"); valeurs.append(state)
    if type is not None: champs.append("type = ?"); valeurs.append(type)
    if coord_x is not None : champs.append("coord_x = ?"); valeurs.append(coord_x)
    if coord_y is not None : champs.append("coord_y = ?"); valeurs.append(coord_y)

    
    if not champs:
        conn.close()
        
    valeurs.append(id)
    try:
        c.execute(f'''UPDATE SEMAPHORES SET {', '.join(champs)} WHERE id = ?''', valeurs)
        conn.commit()
        print("Semaphore avec l'id", id, "a été modifié.")
        return "Semaphore modifié avec succès"
    except Error as e:
        print("Error:", e)
        return "Erreur lors de la modification du semaphore", e
    finally:
        conn.close()
#---------------------------------------------------------------------------------

#------------------------------ Fonctions des Robots ----------------------------------


def list_robots():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM ROBOTS''')
        afficher_robot = [dict(row) for row in c.fetchall()]
        return afficher_robot
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage des robots", e
    finally:
        conn.commit()
        conn.close()
        


def get_robot(id):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM ROBOTS WHERE id = ?''', (id,))
        afficher_robot = [dict(row) for row in c.fetchall()]
        return afficher_robot
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage du robot","de l'id :",id, e
    finally:
        conn.commit()
        conn.close()
        


def get_robot_mission(id):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM MISSION WHERE id_robot = ?''', (id,))
        afficher_robot_mission = [dict(row) for row in c.fetchall()]
        return afficher_robot_mission
    except Error as e:
        print(f"Error: {e}")
        return "Erreur", e
    finally:
        conn.commit()
        conn.close()
        return "Mission affiché avec succès en fonction du robot"


def add_robot(nom,state,speed,position_x,position_y):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, nom, state, speed, position_x, position_y)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO ROBOTS (id, name, state, speed, position_x, position_y) VALUES (?, ?, ?, ?, ?, ?)''',
                 (nouvel_uuid, nom, state, speed, position_x, position_y))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout du robot", e
    conn.commit()
    conn.close()
    return "Robot ajouté avec succès"

def update_robot(id, nom, state, speed, position_x, position_y):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    
    champs = []
    valeurs = []
    
    if nom is not None: champs.append("name = ?"); valeurs.append(nom)
    if state is not None: champs.append("state = ?"); valeurs.append(state)
    if speed is not None: champs.append("speed = ?"); valeurs.append(speed)
    if position_x is not None: champs.append("position_x = ?"); valeurs.append(position_x)
    if position_y is not None: champs.append("position_y = ?"); valeurs.append(position_y)
    
    if not champs:
        conn.close()
        
    valeurs.append(id)
    try:
        c.execute(f'''UPDATE ROBOTS SET {', '.join(champs)} WHERE id = ?''', valeurs)
        conn.commit()
        print("Robot avec l'id", id, "a été modifié.")
        return "Robot modifié avec succès"
    except Error as e:
        print ("Error:",e)
        return "Erreur lors de la modification du robot", e
    finally:
        conn.close()
    
#---------------------------------------------------------------------------------

#------------------------------ Fonctions des Équipes ---------------------------------


def list_equipes():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM TEAMS''')
        afficher_equipe = [dict(row) for row in c.fetchall()]
        return afficher_equipe
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage des équipes", e
    finally:
        conn.commit()
        conn.close()
        

def ajouter_equipe(nom_equipe, ip_equipe,allowed):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, nom_equipe, ip_equipe, allowed)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO TEAMS (id, name, ip, allowed) VALUES (?, ?, ?, ?)''',
              (nouvel_uuid, nom_equipe, ip_equipe, allowed))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout de l'équipe", e 
    conn.commit()
    conn.close()
    return "Équipe ajoutée avec succès"


def modifier_equipe(id, name, ip, allowed):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    
    champs = []
    valeurs = []
    
    if name is not None: champs.append("name = ?"); valeurs.append(name)
    if ip is not None: champs.append("ip = ?"); valeurs.append(ip)
    if allowed is not None: champs.append("allowed = ?"); valeurs.append(allowed)
    
    if not champs:
        conn.close()
    
    valeurs.append(id)
    try:
        c.execute(f'''UPDATE TEAMS SET {', '.join(champs)} WHERE id = ?''', valeurs)
        conn.commit()
        print("L'équipe avec l'id", id, "a été modifiée.")
        return "Equipe modifiée avec succès"
    except Error as e:
        print("Error:", e)
        return "Erreur lors de la modification de l'équipe", e
    finally:
        conn.close()


#---------------------------------------------------------------------------------

#------------------------------ Fonctions des Missions --------------------------------

def get_mission(team):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try : 
        c.execute('''SELECT * FROM MISSIONS WHERE team = ?''', (team,))
        afficher_mission_equipe = [dict(row) for row in c.fetchall()]
        return afficher_mission_equipe
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage de la mission missions", e
    finally:
        conn.commit()
        conn.close()
    

def list_missions():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM MISSIONS''')
        afficher_mission = [dict(row) for row in c.fetchall()]
        return afficher_mission
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage des missions", e
    finally:
        conn.commit()
        conn.close()

def ajouter_mission(name, semaphore_id, robot_id,shape_id, team_id,state, start_date, end_date,team, time):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, name, semaphore_id, robot_id,shape_id, team_id,state, start_date, end_date,team, time)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO MISSIONS (id, name, semaphore_id, robot_id,shapes_id, team_id,state, start_date, end_date,team, time) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)''',
                (nouvel_uuid, name, semaphore_id, robot_id,shape_id, team_id,state, start_date, end_date,team, time))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout de la mission", e 
    conn.commit()
    conn.close()
    return "Mission ajouté avec succès"



def modifier_mission(id, name, semaphore_id, robot_id, shape_id, state, start_date, end_date, team, time):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    
    champs = []
    valeurs = []
    
    if name is not None: champs.append("name = ?"); valeurs.append(name)
    if semaphore_id is not None: champs.append("semaphore_id = ?"); valeurs.append(semaphore_id)
    if robot_id is not None: champs.append("robot_id = ?"); valeurs.append(robot_id)
    if shape_id is not None: champs.append("shapes_id = ?"); valeurs.append(shape_id)
    if state is not None: champs.append("state = ?"); valeurs.append(state)
    if start_date is not None: champs.append("start_date = ?"); valeurs.append(start_date)
    if end_date is not None: champs.append("end_date = ?"); valeurs.append(end_date)
    if team is not None: champs.append("team = ?"); valeurs.append(team)
    if time is not None: champs.append("time = ?"); valeurs.append(time)
    
    if not champs:
        conn.close()
    
    valeurs.append(id)
    
    try:
        c.execute(f'''UPDATE MISSIONS SET {', '.join(champs)} WHERE id = ?''', valeurs)
        conn.commit()
        print("La mission avec l'id :", id, "a été modifiée.")
        return "Mission modifiée avec succès" 
    except Error as e:
        print("Error:", e)
        return "Erreur lors de la modification de la mission", e  
    finally:
        conn.close()
#---------------------------------------------------------------------------------

#------------------------------ Fonctions des Formes ---------------------------------

def list_formes():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SHAPES''')
        afficher_forme = [dict(row) for row in c.fetchall()]
        return afficher_forme
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage des formes", e
    finally:
        conn.commit()
        conn.close()

def get_shape(id):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SHAPES WHERE id = ?''', (id,))
        afficher_forme = [dict(row) for row in c.fetchall()]
        return afficher_forme
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage de la forme","de l'id :",id, e
    finally:
        conn.commit()
        conn.close()
        
    
def ajouter_forme(name, image):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, name, image)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO SHAPES (id, name, image) VALUES (?, ?, ?)''',
              (nouvel_uuid, name, image))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout de la forme", e 
    conn.commit()
    conn.close()
    return "Forme ajoutée avec succès"


def update_shape(id, name, image):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    
    champs = []
    valeurs = []
    
    if name is not None: champs.append("name = ?"); valeurs.append(name)
    if image is not None: champs.append("image = ?"); valeurs.append(image)
    
    if not champs:
        conn.close()
      
    valeurs.append(id)  
    try:
        c.execute(f'''UPDATE SHAPES SET {', '.join(champs)} WHERE id = ?''', valeurs)
        conn.commit()
        return "Forme modifiée avec succès"
    except Error as e:
        return "Erreur lors de la modification :", e   
    finally:
        conn.close()


#---------------------------------------------------------------------------------

#------------------------------ Fonctions des config ---------------------------------

def get_config():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM CONFIG''')
        afficher_config = [dict(row) for row in c.fetchall()]
        return afficher_config
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage des config", e
    finally:
        conn.commit()
        conn.close()

def add_config(grille,nbr_semaphore,nbr_robot):
    conn = sqlite3.connect("Massilia.db")
    config_id = 1
    print(config_id,grille,nbr_semaphore,nbr_robot)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO CONFIG (id, grille,nbr_semaphore,nbr_robot) VALUES (?, ?, ?,?)''',
              (config_id,grille,nbr_semaphore,nbr_robot))
    except Error as e:
        print("Error:",e)
        return "Erreur lors de l'ajout de la config", e 
    conn.commit()
    conn.close()
    return "Config ajoutée avec succès"


def update_config(grille,nbr_semaphore,nbr_robot):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    
    champs = []
    valeurs = []
    
    if grille is not None: champs.append("grille = ?"); valeurs.append(grille)
    if nbr_semaphore is not None: champs.append("nbr_semaphore = ?"); valeurs.append(nbr_semaphore)
    if nbr_robot is not None : champs.append("nbr_robot = ?"); valeurs.append(nbr_robot)
    
    if not champs:
        conn.close()
        
    try:
        c.execute(f'''UPDATE CONFIG SET {', '.join(champs)} WHERE id = 1''', valeurs)
        conn.commit()
        return "Config modifiée avec succès"
    except Error as e:
        return "Erreur lors de la modification de la configuration :",e   
    finally:
        conn.close()
