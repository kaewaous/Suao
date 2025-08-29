"""
kotatsu.py
Descarga y gestión de mangas/manhwas.
Integración con storage_manager y historial.
"""

import os
from datetime import datetime
from modulos import historial, storage_manager
from modulos import chunked_downloader 
DOWNLOAD_PATH = "downloads/mangas/"

# Crear carpeta si no existe
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Simulación de base de datos de mangas (en un producto final podría conectarse a APIs reales)
MANGAS_DB = {
    "naruto": {
        "capitulos": 700,
        "ultimos": [699, 700]
    },
    "one_piece": {
        "capitulos": 1200,
        "ultimos": [1199, 1200]
    }
}

def buscar_manga(nombre: str):
    """
    Busca manga en la base de datos simulada.
    """
    nombre = nombre.lower()
    if nombre in MANGAS_DB:
        info = MANGAS_DB[nombre]
        return {"nombre": nombre, "capitulos": info["capitulos"], "ultimos": info["ultimos"]}
    return None

def descargar_capitulo(nombre_manga: str, capitulo: int, usuario_id: int):
    """
    Simula la descarga de un capítulo de manga.
    Guarda archivo en storage_manager y registra en historial.
    """
    archivo_nombre = f"{nombre_manga}_cap_{capitulo}.cbz"
    archivo_path = os.path.join(DOWNLOAD_PATH, archivo_nombre)

    # Simular descarga creando un archivo vacío
    with open(archivo_path, "w", encoding="utf-8") as f:
        f.write(f"Capítulo {capitulo} de {nombre_manga} descargado el {datetime.now()}")

    # Guardar archivo con storage_manager
    storage_manager.guardar_archivo(archivo_path, categoria="mangas")

    # Registrar en historial
    historial.registrar(usuario_id, archivo_nombre, tipo="mangas", duracion="")  # duracion vacía para mangas

    return f"[kotatsu] Capítulo {capitulo} de {nombre_manga} descargado con éxito."

def descargar_ultimos(nombre_manga: str, usuario_id: int):
    """
    Descarga los últimos capítulos del manga.
    """
    info = buscar_manga(nombre_manga)
    if not info:
        return f"[kotatsu] Manga '{nombre_manga}' no encontrado."

    resultados = []
    for cap in info["ultimos"]:
        resultado = descargar_capitulo(nombre_manga, cap, usuario_id)
        resultados.append(resultado)
    return resultados

def descargar_todos(nombre_manga: str, usuario_id: int):
    """
    Descarga todos los capítulos de un manga.
    """
    info = buscar_manga(nombre_manga)
    if not info:
        return f"[kotatsu] Manga '{nombre_manga}' no encontrado."

    resultados = []
    for cap in range(1, info["capitulos"] + 1):
        resultado = descargar_capitulo(nombre_manga, cap, usuario_id)
        resultados.append(resultado)
    return resultados