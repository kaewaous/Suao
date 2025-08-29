"""
storage_manager.py
Organiza archivos de SouaweakBot y mantiene espacio libre en la laptop.
"""

import os
import shutil
from datetime import datetime

DOWNLOAD_PATH = "downloads/"
LIMITE_GB = 20  # Límite total antes de limpiar

# Carpetas por categoría
CARPETAS = {
    "videos": os.path.join(DOWNLOAD_PATH, "videos"),
    "fotos": os.path.join(DOWNLOAD_PATH, "fotos"),
    "audio": os.path.join(DOWNLOAD_PATH, "audio"),
    "mangas": os.path.join(DOWNLOAD_PATH, "mangas"),
    "otros": os.path.join(DOWNLOAD_PATH, "otros"),
}

# Crear carpetas si no existen
for c in CARPETAS.values():
    os.makedirs(c, exist_ok=True)

def espacio_total_gb(path=DOWNLOAD_PATH):
    """Calcula espacio total ocupado en GB"""
    total_bytes = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_bytes += os.path.getsize(fp)
    return total_bytes / (1024 ** 3)

def limpiar_espacio():
    """
    Si el total supera LIMITE_GB, elimina archivos más antiguos primero.
    """
    total_gb = espacio_total_gb()
    if total_gb <= LIMITE_GB:
        return False

    archivos = []
    for dirpath, dirnames, filenames in os.walk(DOWNLOAD_PATH):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            archivos.append((fp, os.path.getmtime(fp)))

    # Ordenar por fecha de modificación (antiguos primero)
    archivos.sort(key=lambda x: x[1])

    while espacio_total_gb() > LIMITE_GB and archivos:
        file_to_remove, _ = archivos.pop(0)
        try:
            os.remove(file_to_remove)
            print(f"[storage_manager] Archivo eliminado para liberar espacio: {file_to_remove}")
        except:
            pass
    return True

def guardar_archivo(ruta_archivo: str, categoria: str = "otros"):
    """
    Mueve un archivo a la carpeta correspondiente y limpia si es necesario.
    """
    categoria = categoria.lower()
    if categoria not in CARPETAS:
        categoria = "otros"

    # Carpeta destino
    carpeta_destino = CARPETAS[categoria]
    nombre_archivo = os.path.basename(ruta_archivo)
    destino = os.path.join(carpeta_destino, nombre_archivo)

    try:
        shutil.move(ruta_archivo, destino)
        print(f"[storage_manager] Archivo guardado en: {destino}")
    except Exception as e:
        print(f"[storage_manager] Error moviendo archivo {ruta_archivo}: {e}")

    # Limpiar espacio si excede el límite
    limpiar_espacio()
    return destino

def listar_archivos(categoria: str = None):
    """
    Lista archivos en la carpeta de descargas o en una categoría específica.
    """
    archivos_list = []
    if categoria:
        carpeta = CARPETAS.get(categoria.lower(), DOWNLOAD_PATH)
        for f in os.listdir(carpeta):
            archivos_list.append(os.path.join(carpeta, f))
    else:
        for c in CARPETAS.values():
            for f in os.listdir(c):
                archivos_list.append(os.path.join(c, f))
    return archivos_list