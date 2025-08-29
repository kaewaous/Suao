"""
chunked_downloader.py
Descarga de archivos grandes (videos/audio) en partes para optimizar uso de recursos.
Integración directa con downloader.py.
"""

import os
import re
import aiohttp
import asyncio
import psutil  # Para monitoreo de recursos
import logging
from modulos import historial, storage_manager

logger = logging.getLogger(__name__)

CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB por chunk, ajustable

def recursos_disponibles(min_cpu=20, min_ram=200):
    """
    Verifica si hay suficientes recursos para continuar la descarga.
    min_cpu: porcentaje mínimo de CPU libre
    min_ram: MB mínimo de RAM libre
    """
    cpu_libre = 100 - psutil.cpu_percent(interval=0.5)
    ram_libre = psutil.virtual_memory().available / (1024 * 1024)
    return cpu_libre >= min_cpu and ram_libre >= min_ram


async def descargar_chunked(url: str, usuario_id: int, tipo_archivo="video"):
    """
    Descarga un archivo grande en partes (chunked) y lo guarda en la carpeta correspondiente.
    """
    carpeta = "downloads/videos" if tipo_archivo == "video" else "downloads/audio"
    nombre_archivo = os.path.basename(url.split("?")[0])
    nombre_archivo = re.sub(r'[^\w.-]', '_', nombre_archivo)  # Nombre seguro
    ruta_local = os.path.join(carpeta, nombre_archivo)

    os.makedirs(carpeta, exist_ok=True)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return f"❌ Error al acceder a URL: {url}"

                tamaño_total = int(resp.headers.get("Content-Length", 0))
                descargado = 0

                with open(ruta_local, "wb") as f:
                    while True:
                        if not recursos_disponibles():
                            logger.warning(f"[chunked_downloader] Recursos bajos, pausando descarga de {nombre_archivo}")
                            await asyncio.sleep(5)
                            continue

                        chunk = await resp.content.read(CHUNK_SIZE)
                        if not chunk:
                            break
                        f.write(chunk)
                        descargado += len(chunk)
                        porcentaje = (descargado / tamaño_total * 100) if tamaño_total else 0
                        logger.info(f"[chunked_downloader] {nombre_archivo}: {porcentaje:.2f}% descargado")

        # Guardar en storage_manager y registrar historial
        storage_manager.guardar_archivo(ruta_local, tipo_archivo)
        historial.registrar(usuario_id, nombre_archivo, tipo_archivo, url, duracion=0)

        return f"✅ Descarga completa: {nombre_archivo}"

    except Exception as e:
        logger.error(f"[chunked_downloader] Error descargando {url}: {str(e)}")
        return f"❌ Error descargando {nombre_archivo}: {str(e)}"