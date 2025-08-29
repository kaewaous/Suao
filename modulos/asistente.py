import re
from modulos import downloader

URL_REGEX = r'(https?://[^\s]+)'

def manejar_mensaje(usuario, texto):
    if re.match(URL_REGEX, texto):
        return downloader.descargar(texto)  # usar tu módulo
    # ... aquí sigue el resto de comandos (/historial, etc.)