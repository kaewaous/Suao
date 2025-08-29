"""
youtube.py
Descargas especializadas de YouTube: videos individuales y playlists completas.
Integración con storage_manager, historial, chunked_downloader y compressor.
"""

import os
import logging
from modulos import historial, storage_manager, chunked_downloader, compressor
import yt_dlp

DOWNLOAD_PATH = "downloads/videos/"

# Crear carpeta si no existe
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Configurar logging
logging.basicConfig(level=logging.INFO)

def descargar_video(url: str, usuario_id: int, solo_audio=False):
    """
    Descarga un video individual de YouTube.
    """
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if solo_audio else 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'progress_hooks': [hook_progreso]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        titulo = info.get('title', 'video_desconocido')
        ext = info.get('ext', 'mp4')
        duracion = str(info.get('duration', ''))

        # Determinar tipo
        tipo = "audio" if solo_audio else "videos"

        archivo_path = os.path.join(DOWNLOAD_PATH, f"{titulo}.{ext}")

        # Guardar archivo en storage_manager
        storage_manager.guardar_archivo(archivo_path, tipo)

        # Registrar en historial
        historial.registrar(usuario_id, titulo, tipo=tipo, url=url, duracion=duracion)

        return f"[youtube] {tipo.capitalize()} descargado: {titulo}"

    except Exception as e:
        logging.error(f"[youtube] Error descargando {url}: {e}")
        # Aquí se podría integrar chunked_downloader o un método alternativo
        return f"[youtube] Error descargando {url}: {e}"

def descargar_playlist(url: str, usuario_id: int, solo_audio=False):
    """
    Descarga todos los videos de una playlist de YouTube.
    """
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if solo_audio else 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'ignoreerrors': True,
        'progress_hooks': [hook_progreso]
    }

    resultados = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            entries = info.get('entries', [])

            for video in entries:
                if video is None:
                    continue
                titulo = video.get('title', 'video_desconocido')
                ext = video.get('ext', 'mp4')
                duracion = str(video.get('duration', ''))
                tipo = "audio" if solo_audio else "videos"
                archivo_path = os.path.join(DOWNLOAD_PATH, f"{titulo}.{ext}")

                # Guardar y registrar
                storage_manager.guardar_archivo(archivo_path, tipo)
                historial.registrar(usuario_id, titulo, tipo=tipo, url=video.get('webpage_url', ''), duracion=duracion)

                resultados.append(f"[youtube] {tipo.capitalize()} descargado: {titulo}")

        return resultados

    except Exception as e:
        logging.error(f"[youtube] Error descargando playlist {url}: {e}")
        return [f"[youtube] Error descargando playlist: {e}"]

def hook_progreso(d):
    """
    Hook para mostrar progreso o integrarlo con futuros features.
    """
    if d['status'] == 'finished':
        logging.info(f"[youtube] Descarga completada: {d['filename']}")
    elif d['status'] == 'downloading':
        pct = d.get('_percent_str', '0%')
        logging.info(f"[youtube] Descargando {d['filename']}: {pct}")