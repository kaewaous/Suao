"""
parallel_downloader.py
Descarga simultánea de múltiples archivos (videos, audios, fotos) usando asyncio.
Integra chunked_downloader para archivos grandes.
"""

import asyncio
from modulos import chunked_downloader, downloader, historial, resource_manager

async def descargar_varias(urls: list, usuario_id: int):
    """
    Descarga múltiples URLs en paralelo.
    """
    tareas = []

    for url in urls:
        # Revisar tamaño estimado o tipo para usar chunked_downloader si es grande
        # Por simplicidad asumimos que todo video grande usa chunked
        if url.endswith((".mp4", ".mkv", ".avi")):  # archivos de video
            tareas.append(chunked_downloader.descargar_chunked(url, usuario_id, tipo_archivo="video"))
        elif url.endswith((".mp3", ".wav")):  # archivos de audio
            tareas.append(chunked_downloader.descargar_chunked(url, usuario_id, tipo_archivo="audio"))
        else:
            # Para fotos u otros, usar downloader normal
            tareas.append(downloader.descargar_archivo(url, usuario_id))

    resultados = await asyncio.gather(*tareas)
    return resultados