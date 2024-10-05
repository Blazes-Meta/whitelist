import sqlite3
from lib.mojang import *

class NoEntryError(Exception):
    ...

class Player:
    def __init__(self, dcid, uuid):
        self.dcid = dcid
        self.uuid = uuid

    def fromminecraftname(dcid: int, minecraftname: str):
        uuid = getUUID(minecraftname)
        return Player(dcid=dcid, uuid=uuid)
    
    def minecraftname(self) -> str:
        return getPlayername(self.uuid)

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

    def playerbaseSet(self, player: Player) -> None:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        if not self.playerExists(player.dcid):
            cursor.execute("INSERT INTO player (DcID, UUID) VALUES (?, ?)", (player.dcid, player.uuid))
        else:
            cursor.execute("UPDATE player SET UUID = ? WHERE DcID = ?", (player.dcid, player.uuid))
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
        uuid = getPlayername(result[0])

        if result:
            return Player(dcid=dcid, uuid=uuid)
        else:
            raise NoEntryError("Spieler nicht registriert")
        
    def playerbaseList(self) -> list[Player]:
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT DcID, UUID FROM player ORDER BY ASC")
        rows = cursor.fetchall()
        conn.close()
        result = []
        for row in rows:
            result.append(Player(dcid=row[0], uuid=row[1]))
        return result