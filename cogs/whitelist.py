import sqlite3

# Verbindung zu SQLite herstellen
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Tabelle erstellen
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')

# Daten einfügen
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
conn.commit()

# Daten abfragen
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())

# Verbindung schließen
conn.close()
