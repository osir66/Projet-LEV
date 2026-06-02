import base_projet
import sqlite3
from sqlite3 import Error

def ajouter_semaphore(id, etat, dessin_forme, matrice):
    conn = sqlite3.connect("Massilia.db")
    print(id, etat, dessin_forme, matrice)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO SEMAPHORE (id, etat, dessin_forme, matrice) VALUES (?, ?, ?, ?)''',
              (id, etat, dessin_forme, matrice))
    except Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

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
    finally:
        conn.close()

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
    finally:
        conn.close()    

def ajouter_robot(id, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement):
    conn = sqlite3.connect("Massilia.db")
    print(id, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement)
    try :
        c = conn.cursor()
        c.execute('''INSERT INTO ROBOT (id, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement) VALUES (?, ?, ?, ?, ?)''',
              (id, position_actuelle_x, position_actuelle_y, est_disponible, vitesse_deplacement))
    except Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

def supprimer_robot(id):
    conn = sqlite3.connect("Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''DELETE FROM ROBOT WHERE id = ?''', (id,))
        conn.commit()
        print("Robot avec l'id",id, "a été supprimé.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        