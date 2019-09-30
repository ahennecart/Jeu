import sqlite3

cur = sqlite3.connect("Test.db").cursor()
cur.execute("""SELECT * FROM Ville WHERE Cartier == 'CV' """)
liste = cur.fetchall()
print(liste)
