from discord import app_commands

# Diese Exception-Klassen sind dafür, dass ich Errors in App Commands richtig handlen kann 

class AppPermissionError(app_commands.AppCommandError):
    """Fehler, wenn ein Benutzer keine Berechtigungen hat."""
    ...

class MissingAppArgument(app_commands.AppCommandError):
    """Fehler, wenn ein optionales Argument fehlt, aber trotzdem benötigt wird."""
    ...

class AppAPIError(app_commands.AppCommandError):
    ...

class GithubError(app_commands.AppCommandError):
    ...

class AlreadyExists(app_commands.AppCommandError):
    ...

class DoesntExist(app_commands.AppCommandError):
    ...