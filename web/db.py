import base_projet
import sqlite3
from sqlite3 import Error
import uuid

def ajouter_semaphore(etat, dessin_forme, matrice):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(id, etat, dessin_forme, matrice)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO SEMAPHORE (id, etat, dessin_forme, matrice) VALUES (?, ?, ?, ?)''',
              (nouvel_uuid, etat, dessin_forme, matrice))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout du semaphore", e
    conn.commit()
    conn.close()
    return "Semaphore ajouté avec succès"

def afficher_semaphore():
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SEMAPHORE''')
        afficher_semaphore = c.fetchall()
        return afficher_semaphore
    except Error as e:
        print(f"Error: {e}")
        conn.close()

def supprimer_semaphore(id):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''DELETE FROM SEMAPHORE WHERE id = ?''', (id,))
        conn.commit()
        print("Semaphore avec l'id",id, "a été supprimé.")
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de la suppression du semaphore", e
    finally:
        conn.close()
        return "Semaphore supprimé avec succès"

def modifier_semaphore(id, etat, dessin_forme, matrice):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''UPDATE SEMAPHORE SET etat = ?, dessin_forme = ?, matrice = ? WHERE id = ?''',
              (etat, dessin_forme, matrice, id))
        conn.commit()
        print("Semaphore avec l'id",id, "a été modifié.")
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de la modification du semaphore", e
    finally:
        conn.close()  
        return "Semaphore modifié avec succès"  

def ajouter_robot(nom_robot, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, nom_robot, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO ROBOT (id, nom_robot, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement) VALUES (?, ?, ?, ?, ?, ?)''',
              (nouvel_uuid, nom_robot, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout du robot", e
    conn.commit()
    conn.close()
    return "Robot ajouté avec succès"

def supprimer_robot(id):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''DELETE FROM ROBOT WHERE id = ?''', (id,))
        conn.commit()
        print("Robot avec l'id",id, "a été supprimé.")
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de la suppression du robot", e
    finally:
        conn.close()
        return "Robot supprimé avec succès"

def afficher_robot():
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM ROBOT''')
        afficher_robot = c.fetchall()
        return afficher_robot
    except Error as e:
        print(f"Error: {e}")
        conn.close()

   
def ajouter_equipe(nom_equipe, ip_equipe):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, nom_equipe, ip_equipe)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO EQUIPE (id, nom_equipe, ip_equipe) VALUES (?, ?, ?)''',
              (nouvel_uuid, nom_equipe, ip_equipe))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout de l'équipe", e 
    conn.commit()
    conn.close()
    return "Equipe ajouté avec succès"

def ajouter_forme(type_forme):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, type_forme)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO FORME (id, type_forme) VALUES (?, ?)''',
              (nouvel_uuid, type_forme))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout de la forme", e 
    conn.commit()
    conn.close()
    return "Forme ajouté avec succès"

def afficher_forme():
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try : 
        c.execute('''SELECT * FROM FORME''')
        afficher_forme = c.fetchall()
        return afficher_forme
    except Error as e:
        print(f"Error: {e}")
        conn.close()

def ajouter_mission(id_semaphore, id_forme, id_robot, status, heure_exec):
    conn = sqlite3.connect("Massilia.db")
    nouvel_uuid = str(uuid.uuid4())
    print(nouvel_uuid, id_semaphore, id_forme, id_robot, status, heure_exec)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO MISSION (id, id_semaphore, id_forme, id_robot, status, heure_exec) VALUES (?, ?, ?, ?, ?, ?)''',
              (nouvel_uuid, id_semaphore, id_forme, id_robot, status, heure_exec))
    except Error as e:
        print(f"Error: {e}")
        return "Erreur lors de l'ajout de la mission", e 
    conn.commit()
    conn.close()
    return "Mission ajouté avec succès"