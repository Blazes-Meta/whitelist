import sqlite3

def playerbaseGet(dcid: int) -> str:
    conn = sqlite3.connect('playerbase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT UUID FROM player WHERE DcID = ?", (dcid,))
    result = cursor.fetchone()
    conn.commit()
    conn.close()

    if result:
        return result[0]
    else:
        raise Exception("Spieler nicht registriert")
    
print(playerbaseGet(720992368110862407))