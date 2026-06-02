import base_projet
import sqlite3
from sqlite3 import Error

def ajouter_semaphore(id, etat, dessin_forme, matrice):
    conn = sqlite3.connect("../Massilia.db")
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
    conn = sqlite3.connect("../Massilia.db")
    c = conn.cursor()
    try :
        c.execute('''SELECT * FROM SEMAPHORE''')
        afficher_semaphore = c.fetchall()
        return afficher_semaphore
    except Error as e:
        print(f"Error: {e}")
        conn.close()
        