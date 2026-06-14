import sqlite3
from sqlite3 import Error

#création des tables 
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
                        position_x REAL NOT NULL DEFAULT 0,
                        position_y REAL NOT NULL DEFAULT 0 
                )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS SEMAPHORES (
                        id TEXT PRIMARY KEY,
                        name TEXT,
                        state TEXT DEFAULT 'Available',
                        duration INTEGER,
                        type TEXT,
                        coord_x INTEGER,
                        coord_y INTEGER 
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
            nbr_robot      INTEGER NOT NULL,
            nombre_x       INTEGER NOT NULL, 
            nombre_y       INTEGER NOT NULL
        )''')

        c.execute('''CREATE TABLE IF NOT EXISTS SEGMENT (
                  id TEXT PRIMARY KEY,
                  coord_a_x  INTEGER NOT NULL,
                  coord_a_y  INTEGER NOT NULL,
                  coord_b_x  INTEGER NOT NULL,
                  coord_b_y  INTEGER NOT NULL,
                  UNIQUE (coord_a_x, coord_a_y, coord_b_x, coord_b_y)
        )''')

        conn.commit()
        print("Tables créées avec succès")
    except Error as e:
        print("Erreur lors de la création des tables : ", e)
    finally:
        conn.close()


#table()








