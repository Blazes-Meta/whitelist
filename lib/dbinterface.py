import sqlite3
from lib.mojang import *
import os

class NoEntryError(Exception):
    ...

class Playerbase:
    def __init__(self, dbpath: str = "tmp/playerbase.db"):
        self.dbpath = dbpath
        if not os.path.exists(os.path.dirname(dbpath)):
            os.makedirs(os.path.dirname(dbpath))
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS player (DcID INTEGER PRIMARY KEY, UUID TEXT NOT NULL)')
        cursor.execute('CREATE TABLE IF NOT EXISTS whitelist (DcID INTEGER PRIMARY KEY)')
        conn.commit()
        conn.close()

    def entryExists(self, dcid: int) -> bool:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM player WHERE DcID = ?", (dcid,))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return False
        return True

    def setPlayer(self, dcid: int, uuid: str) -> None:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        if not self.entryExists(dcid):
            cursor.execute("INSERT INTO player (DcID, UUID) VALUES (?, ?)", (dcid, uuid))
        else:
            cursor.execute("UPDATE player SET UUID = ? WHERE DcID = ?", (uuid, dcid))
        conn.commit()
        conn.close()
        
    def removePlayer(self, dcid: int) -> None:
        if self.entryExists(dcid):
            conn = sqlite3.connect(self.dbpath)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM player WHERE DcID = ?", (dcid,))
            conn.commit()
            conn.close()
        else:
            raise NoEntryError("Kein Spieler vorhanden")
        
    def getPlayerUUID(self, dcid: int) -> str:
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
        
    def list(self) -> dict:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT DcID, UUID FROM player")
        rows = cursor.fetchall()
        conn.close()
        result = {row[0]: row[1] for row in rows}
        return result
    
    def isonWhitelist(self, dcid: int) -> bool:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM whitelist WHERE DcID = ?", (dcid,))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return False
        return True
    
    def whitelistAdd(self, dcid: int) -> None:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO whitelist (DcID) VALUES (?)", (dcid,))
        conn.commit()
        conn.close()

    def whitelistRemove(self, dcid: int) -> None:
        if self.isonWhitelist(dcid):
            conn = sqlite3.connect(self.dbpath, timeout=5)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM whitelist WHERE DcID = ?", (dcid,))
            conn.commit()
            conn.close()
        else:
            raise NoEntryError("Kein Spieler vorhanden")