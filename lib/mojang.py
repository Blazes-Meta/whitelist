import requests

MOJANG_API = "https://api.mojang.com/users/profiles/minecraft"
MOJANG_SESSIONSERVER = f"https://sessionserver.mojang.com/session/minecraft/profile"

class MojangAPIError(Exception): ...

def getUUID(playername: str) -> str:
    response = requests.get(f"{MOJANG_API}/{playername}")
    if response.status_code == 200:
        data = response.json()
        return data['id']
    raise MojangAPIError("UUID konnte nicht erhalten werden")
    
def getPlayername(uuid: str) -> str:
    response = requests.get(f"{MOJANG_SESSIONSERVER}/{uuid}")
    if response.status_code == 200:
        data = response.json()
        return data['name']
    raise MojangAPIError("Spielername konnte nicht erhalten werden")