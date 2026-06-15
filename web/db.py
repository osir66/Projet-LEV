import base_projet
import sqlite3
from sqlite3 import Error
import uuid
import urllib.request
from pathlib import Path

#------------------------------ Fonctions des Sémaphores ----------------------------------

#fonction qui permet d'afficher les sémaphores
def list_semaphore():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row                              
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SEMAPHORES''')
        afficher_semaphore = [dict(row) for row in c.fetchall()] #convertit chaque ligne retournées par la requete en dictionnaire Python
        print (afficher_semaphore)
        return afficher_semaphore
    except Error as e:
        print("Error:",e)
        return "Erreur de l'affichage des semaphores", e
    finally:
        conn.commit()
        conn.close()
        

#fonction qui permet d'afficher un sémaphore en fonction de l'id
def get_semaphore(id):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SEMAPHORES WHERE id = ?''', (id,))
        afficher_semaphore = [dict(row) for row in c.fetchall()] #convertit chaque ligne retournées par la requete en dictionnaire Python
        return afficher_semaphore
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage du semaphore","de l'id :",id, e
    finally:
        conn.commit()
        conn.close()

#fonction qui permet d'ajouter un sémaphore 
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

#fonction qui permet de modifier un sémaphore en fonction de l'id
def update_semaphore(id, nom, duration, state, type,coord_x,coord_y):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    
    champs = []         #création d'une liste qui contriendra les champs à modifier 
    valeurs = []        #création d'une liste qui contriendra les valeurs correspondante 
    
    #vérifie chaque paramètre 
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

#fonction qui permet d'afficher les robots 
def list_robots():
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM ROBOTS''')
        afficher_robot = [dict(row) for row in c.fetchall()]   #convertit chaque ligne retournées par la requete en dictionnaire Python
        return afficher_robot
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage des robots", e
    finally:
        conn.commit()
        conn.close()
        

#fonction qui permet d'afficher un robot en fonction de son id 
def get_robot(id):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM ROBOTS WHERE id = ?''', (id,))
        afficher_robot = [dict(row) for row in c.fetchall()]        #convertit chaque ligne retournées par la requete en dictionnaire Python
        return afficher_robot
    except Error as e:
        print(f"Error: {e}")
        return "Erreur de l'affichage du robot","de l'id :",id, e
    finally:
        conn.commit()
        conn.close()
        

#fonction qui permet de récuper les missions associés a un robot 
def get_robot_mission(id):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM MISSION WHERE id_robot = ?''', (id,))
        afficher_robot_mission = [dict(row) for row in c.fetchall()]        #convertit chaque ligne retournées par la requete en dictionnaire Python
        return afficher_robot_mission
    except Error as e:
        print(f"Error: {e}")
        return "Erreur", e
    finally:
        conn.commit()
        conn.close()
        return "Mission affiché avec succès en fonction du robot"


#fonction qui permet d'ajouter un robot 
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

#fonction qui permet de modifier un robot en fonction de l'id
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

#fonction qui permet d'afficher les équipes 
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
        
#fonction qui permet d'ajouter une équipe 
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

#fonction qui permet de modifier une équipe 
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

#fonction qui récupère les missions appartenant à une équipe 
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
    
#fonction qui permet d'afficher les missions 
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

#fonction qui permet d'ajouter une mission 
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


#fonction qui permet de modifier une mission en fonction de l'id
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

#fonction qui permet de supprimer la table Missions
def delete_missions_table():
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try:
        c.execute('''DROP TABLE IF EXISTS MISSIONS''')
        conn.commit()
        print("Table MISSIONS supprimée avec succès")
        return "Table MISSIONS supprimée avec succès"
    except Error as e:
        print("Error:", e)
        return "Erreur lors de la suppression de la table MISSIONS", e
    finally:
        conn.close()

#---------------------------------------------------------------------------------

#------------------------------ Fonctions des Formes ---------------------------------

#fonction qui permet d'afficher les formes 
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

#fonction qui permet d'afficher une forme en fonction de l'id
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
        
#fonction qui permet d'ajouter une forme  
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

#fonction qui permet de modifier une forme en fonction de l'id
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

#fonction qui permet d'importer le csv 
def import_csv(csv):
    fichier = Path(csv)
    if not fichier.exists():
        return None
    contenu = fichier.read_text(encoding="utf-8").strip()
    lignes = contenu.splitlines()
    if not lignes:
        return None
    name = lignes[0].strip()
    image = "\n".join(lignes[1:])
    return ajouter_forme(name, image)


#---------------------------------------------------------------------------------

#------------------------------ Fonctions des config ---------------------------------

#fonction qui permet d'afficher la configuration 
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

#fonction qui permet d'ajouter une configuration
def add_config(grille,nbr_semaphore,nbr_robot,nb_x,nb_y):
    conn = sqlite3.connect("Massilia.db")
    print(grille,nbr_semaphore,nbr_robot,nb_x,nb_y)
    try :
        c = conn.cursor()
        c.execute('''REPLACE INTO CONFIG (id,grille,nbr_semaphore,nbr_robot,nombre_x,nombre_y) VALUES (1,?, ?,?,?,?)''',
              (grille,nbr_semaphore,nbr_robot,nb_x,nb_y))
    except Error as e:
        print("Erreur:",e)
        return "Erreur lors de l'ajout de la config", e 
    conn.commit()
    conn.close()
    return "Config ajoutée avec succès"

#fonction qui permet de créer la grille avec les segments 
def faire_grille(name):
    conn = sqlite3.connect("Massilia.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    try:
        #Récupérer la configuration
        c.execute('''SELECT * FROM CONFIG WHERE id = 1''')
        row = c.fetchone()
        
        if not row:
            return "Aucune configuration trouvée."
            
        config = dict(row)
        nombre_x = int(config["nombre_x"])
        nombre_y = int(config["nombre_y"])
        
        c.execute("UPDATE CONFIG SET grille = ? WHERE id = 1", (name,))
        c.execute("DELETE FROM SEGMENT")
        
        # Nouvelles limites 
        offset_x = nombre_x // 2 
        x_min = -offset_x                    
        x_max = nombre_x - offset_x - 1        
        
        y_min = 1                              
        y_max = nombre_y                      
        
        segments = []
        
        segments.append((str(uuid.uuid4()), 0, 0, 0, y_min))
        
        #  Créer les segments de la grille 
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                if x < x_max:
                    segments.append((str(uuid.uuid4()), x, y, x + 1, y))
                if y < y_max:
                    segments.append((str(uuid.uuid4()), x, y, x, y + 1))
                    
        #Insertion des segments dans la table SEGMENT
        if segments:
            c.executemany(
                "INSERT INTO SEGMENT (id, coord_a_x, coord_a_y, coord_b_x, coord_b_y) VALUES (?, ?, ?, ?, ?)",
                segments)
        conn.commit()
        return "Segment ajouté" 
    except Exception as e:
        print("Erreur :", e)
        return "Erreur :",e
    finally:
        conn.close()

#Fonction qui permet d'afficher les segments 
def afficher_seg():
    conn = sqlite3.connect("Massilia")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SEGMENT''')
        afficher_segment = [dict(row) for row in c.fetchall()]
        return afficher_segment
    except Error as e:
        print("Erreur :",e)
        return "Erreur de l'affichage des segments", e
    finally:
        conn.commit()
        conn.close()

#------------------------------ Fonctions de comptage (API externe) -------------------

BASE_URL = "http://127.168.1.96"

def _fetch_count(endpoint):
    try:
        with urllib.request.urlopen(f"{BASE_URL}{endpoint}", timeout=3) as r:
            return r.read().decode().count('"id"')
    except Exception:
        return "?"

def count_robots():
    return _fetch_count("/api/list_robots")

def count_semaphores():
    return _fetch_count("/api/list_semaphore")

def count_formes():
    return _fetch_count("/api/list_shapes")

def count_missions():
    return _fetch_count("/api/list_missions")

#------------------------------ Fonction Healthcheck ---------------------------------

#fonction qui permet de vérifier la connexion à la base de donnée 
def healthcheck():
    conn = sqlite3.connect("Massilia.db")
    try:
        c = conn.cursor()
        c.execute('''SELECT 1''')
        return "Connexion établie"
    except Error as e:
        return "Erreur de connexion :",e
    finally:
        conn.close()

