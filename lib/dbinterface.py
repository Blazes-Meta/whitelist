import sqlite3
from lib.mojang import *

class NoEntryError(Exception):
    ...

class Playerbase:
    def __init__(self, dbpath: str = "playerbase.db"):
        self.dbpath = dbpath
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS player (DcID INTEGER PRIMARY KEY, UUID TEXT NOT NULL)')
        conn.commit()
        conn.close()

    def playerExists(self, dcid: int) -> bool:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM player WHERE DcID = ?", (dcid,))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return False
        return True

    def playerbaseSet(self, dcid: int, playername: str) -> None:
        uuid = getUUID(playername)
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        if not self.playerExists(dcid):
            cursor.execute("INSERT INTO player (DcID, UUID) VALUES (?, ?)", (dcid, uuid))
        else:
            cursor.execute("UPDATE player SET UUID = ? WHERE DcID = ?", (uuid, dcid))
        conn.commit()
        conn.close()
        
    def playerbaseRemove(self, dcid: int) -> None:
        if self.playerExists(dcid):
            conn = sqlite3.connect(self.dbpath)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM player WHERE DcID = ?", (dcid,))
            conn.commit()
            conn.close()
        else:
            raise NoEntryError("Kein Spieler vorhanden")
        
    def playerbaseGet(self, dcid: int) -> str:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT UUID FROM player WHERE DcID = ?", (dcid,))
        result = cursor.fetchone()
        conn.commit()
        conn.close()

        if result:
            return result[0]
        else:
            raise NoEntryError("Spieler nicht registriert")
        
    def playerbaseList(self) -> dict:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT DcID, UUID FROM player")
        rows = cursor.fetchall()
        result = {row[0]: row[1] for row in rows}
        #result = [f"<@{row[0]}> - {getPlayername(row[1])}" for row in rows]
        conn.close()
        return result