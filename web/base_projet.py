import sqlite3
from sqlite3 import Error

def table():
    try:
        conn = sqlite3.connect("Massilia.db")
        conn.execute("PRAGMA foreign_keys = 1")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS ROBOTS (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        state TEXT,
                        speed INTEGER NOT NULL DEFAULT 1,
                        position_x INTEGER NOT NULL DEFAULT 0,
                        position_y INTEGER NOT NULL DEFAULT 0 
                )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS SEMAPHORES (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        state TEXT DEFAULT 'Available',
                        duration INTEGER,
                        type TEXT
                )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS SHAPES (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        image TEXT
                )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS MISSIONS (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        semaphore_id TEXT,
                        robot_id TEXT,
                        shapes_id TEXT,
                        team_id TEXT,
                        state TEXT,
                        start_date TEXT,
                        end_date TEXT,
                        team TEXT,
                        time TEXT,
                        FOREIGN KEY (semaphore_id) REFERENCES semaphores(id),
                        FOREIGN KEY (robot_id) REFERENCES robots(id),
                        FOREIGN KEY (shapes_id) REFERENCES shapes(id),
                        FOREIGN KEY (team_id) REFERENCES teams(id)
                )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS TEAMS (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        ip TEXT,
                        allowed INTEGER                     
                )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS CONFIG (
            id             INTEGER PRIMARY KEY CHECK (id = 1),
            grille         TEXT NOT NULL,
            nbr_semaphore  INTEGER NOT NULL,
            nbr_robot      INTEGER NOT NULL
        )''')

        conn.commit()
        print("Tables créées avec succès")
    except Error as e:
        print("Erreur lors de la création des tables : ", e)
    finally:
        conn.close()




#table()









