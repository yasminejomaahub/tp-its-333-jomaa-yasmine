import sqlite3
import os
DB = os.path.join(os.path.dirname(__file__), "database.db")
con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("SELECT * FROM etudiants")
print(cur.fetchall())
print("Chemin de la base :", os.path.abspath(DB))
con.close()