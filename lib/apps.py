from discord import app_commands

# Diese Exception-Klassen sind dafür, dass ich Errors in App Commands richtug handlen kann 

class AppPermissionError(app_commands.AppCommandError):
    """Fehler, wenn ein Benutzer keine Berechtigungen hat."""
    ...

class MissingAppArgument(app_commands.AppCommandError):
    """Fehler, wenn ein optionales Argument fehlt, aber trotzdem benötigt wird."""
    ...

class NoEntryFound(app_commands.AppCommandError):
    """Fehler, wenn in der Datenbank kein Eintrag gefunden werden konnte"""
    ...

class AppAPIError(app_commands.AppCommandError):
    ...