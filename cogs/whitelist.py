import sqlite3

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        log(f"[COGS] {__name__} is ready")

    def getUUID(username: str) -> str:
		     ...
    def get username(uuid: str) -> str:
        ...


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

async def setup(bot):
    await bot.add_cog(Whitelist(bot))