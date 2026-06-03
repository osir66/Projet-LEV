import sqlite3
from sqlite3 import Error

def table():
    try:
        conn = sqlite3.connect("Massilia.db")
        conn.execute("PRAGMA foreign_keys = 1")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ROBOT(
                        id TEXT PRIMARY KEY,
                        position_actuelle_x REAL,
                        position_actuelle_y REAL,
                        est_disponible BOOLEAN,
                        vitesse_deplacement REAL    
                    )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS SEMAPHORE(
                        id TEXT PRIMARY KEY,
                        etat BOOLEAN,
                        dessin_forme TEXT,
                        matrice REAL
                    )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS FORME(
                        id TEXT,
                        type_forme TEXT
                    )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS MISSION(
                        id TEXT PRIMARY KEY,
                        id_semaphore TEXT,
                        id_forme TEXT,
                        id_robot TEXT,
                        status TEXT,
                        heure_exec DATETIME,
                        FOREIGN KEY (id_semaphore) REFERENCES SEMAPHORE(id),
                        FOREIGN KEY (id_forme) REFERENCES FORME(id),
                        FOREIGN KEY (id_robot) REFERENCES ROBOT(id)
                    )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS EQUIPE(
                        id TEXT PRIMARY KEY,
                        nom_equipe TEXT,
                        ip_equipe TEXT                        
                    )''')

        conn.commit()
        (print("Tables créées avec succès"))
    except Error as e:
        print("Erreur lors de la création des tables : ",e)
    finally:
        conn.close()

#table()

