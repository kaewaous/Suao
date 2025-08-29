"""
chunked_downloader.py
Descarga de archivos grandes (videos/audio) en partes para optimizar uso de recursos.
Integración directa con downloader.py y resource_manager.py
"""

import os
import aiohttp
import asyncio
from modulos import historial, resource_manager, storage_manager

CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB por chunk, ajustable

async def descargar_chunked(url: str, usuario_id: int, tipo_archivo="video"):
    """
    Descarga un archivo grande en partes (chunked) y lo guarda en la carpeta correspondiente.
    """
    # Selección de carpeta según tipo
    carpeta = "downloads/videos" if tipo_archivo == "video" else "downloads/audio"
    nombre_archivo = url.split("/")[-1]
    ruta_local = os.path.join(carpeta, nombre_archivo)

    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return f"❌ Error al acceder a URL: {url}"

            tamaño_total = int(resp.headers.get("Content-Length", 0))
            descargado = 0

            with open(ruta_local, "wb") as f:
                while True:
                    if not resource_manager.verificar_recursos():
                        await asyncio.sleep(5)  # Pausar si recursos bajos
                        continue

                    chunk = await resp.content.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)
                    descargado += len(chunk)
                    # Mostrar progreso en consola
                    print(f"[chunked_downloader] {nombre_archivo}: {descargado}/{tamaño_total} bytes descargados")

    # Guardar en almacenamiento y limpiar si es necesario
    storage_manager.guardar_archivo(ruta_local)
    historial.guardar_historial(usuario_id, ruta_local, tipo_archivo, f"Descarga chunked completa de {url}")

    return f"✅ Descarga completa: {nombre_archivo}"