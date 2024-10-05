import sqlite3

def playerbaseList() -> dict[int:str]:
    conn = sqlite3.connect("playerbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DcID, UUID FROM player")
    rows = cursor.fetchall()
    result = {row[0]: row[1] for row in rows}
    conn.close()
    return result

print(playerbaseList())