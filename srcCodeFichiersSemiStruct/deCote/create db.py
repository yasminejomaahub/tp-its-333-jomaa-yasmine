import sqlite3

conn = sqlite3.connect ( 'database.db' )
print ("Base de données ouverte avec succès")

conn.execute ( 'CREATE TABLE etudiants (nom TEXT, addr TEXT, pin TEXT)' )
print ("Table créée avec succès")
conn.close ()