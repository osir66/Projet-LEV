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


def add_semaphore(nom, duration, type):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, nom, duration, type)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO SEMAPHORES (id,name,duration,type) VALUES (?, ?, ?, ?)''',
              (nouvel_uuid, nom, duration, type))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout du semaphore", e
    conn.commit()
    conn.close()
    return "Semaphore ajouté avec succès"


def update_semaphore(id,nom,duration,state,type):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''UPDATE SEMAPHORES SET name = ?, duration = ?, state = ?, state = ? WHERE id = ?''',
              (nom, duration, state,type, id))
        conn.commit()
        print("Semaphore avec l'id",id, "a été modifié.")
    except Error as e:
        print("Error:",e)
        return "Erreur lors de la modification du semaphore", e
    conn.close()  
    return "Semaphore modifié avec succès"  

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

def update_robot(id,nom,state,speed,position_x,position_y):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''UPDATE ROBOTS SET name = ?, state = ?, speed = ?, position_x = ?, position_y = ? WHERE id = ?''',
                 (nom, state, speed, position_x, position_y, id))
        conn.commit()
        print("Robot avec l'id",id, "a été modifié.")
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de la modification du robot", e
    conn.commit()
    conn.close()  
    return "Robot modifié avec succès"
    
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

def modifier_equipe(id,ip):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''UPDATE TEAMS SET ip = ? WHERE id = ?''',
              (ip, id))
        conn.commit()
        print("L'équipe avec l'id",id, "a été modifié.")
    except Error as e:
        print("Error:",e)
        return "Erreur lors de la modification de l'équipe", e
    conn.close()  
    return "Equipe modifié avec succès"


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

def ajouter_mission(name, semaphore_id, robot_id,shapes_id, team_id,state, start_date, end_date,team, time):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, name, semaphore_id, robot_id,shapes_id, team_id,state, start_date, end_date,team, time)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO MISSIONS (id, name, semaphore_id, robot_id,shapes_id, team_id,state, start_date, end_date,team, time) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)''',
                (nouvel_uuid, name, semaphore_id, robot_id,shapes_id, team_id,state, start_date, end_date,team, time))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout de la mission", e 
    conn.commit()
    conn.close()
    return "Mission ajouté avec succès"

def modifier_mission(id, state):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try:
        c.execute('''UPDATE MISSIONS 
                     SET state = COALESCE(?, state) 
                     WHERE id = ?''',
                  (state, id))
        
        conn.commit()
        print("La mission avec l'id",id, "a été modifiée.")
        return ("Mission modifié :", id)
    except Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()  
    return "Mission modifié"
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


        