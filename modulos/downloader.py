"""
downloader.py
Descarga total de contenido multimedia de cualquier red social.
Integración con storage_manager, historial, chunked_downloader, parallel_downloader y compressor.
"""

import os
import logging
from modulos import historial, storage_manager
from modulos import chunked_downloader, parallel_downloader, compressor
import yt_dlp

# Carpeta central de descargas
DOWNLOAD_PATH = "downloads/"

# Configurar logging para errores
logging.basicConfig(level=logging.INFO)

def descargar(url: str, usuario_id: int):
    """
    Descarga cualquier URL de red social y guarda archivo en la carpeta correspondiente.
    Detecta tipo de contenido y registra en historial.
    """
    try:
        # Configuración avanzada de yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': False,
            'quiet': True,
            'progress_hooks': [hook_progreso]
        }

        info = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        # Detectar tipo de contenido
        ext = info.get('ext', '')
        titulo = info.get('title', 'archivo_desconocido')
        duracion = str(info.get('duration', ''))

        if ext in ['mp4', 'mkv', 'webm']:
            categoria = "videos"
        elif ext in ['mp3', 'm4a', 'wav']:
            categoria = "audio"
        elif ext in ['jpg', 'png', 'jpeg', 'gif', 'webp']:
            categoria = "fotos"
        else:
            categoria = "otros"

        archivo_path = os.path.join(DOWNLOAD_PATH, f"{titulo}.{ext}")

        # Guardar archivo en storage_manager
        storage_manager.guardar_archivo(archivo_path, categoria)

        # Registrar en historial
        historial.registrar(usuario_id, titulo, tipo=categoria, url=url, duracion=duracion)

        return f"[downloader] {categoria.capitalize()} descargado: {titulo}"

    except Exception as e:
        logging.error(f"[downloader] Error descargando {url}: {e}")
        # Aquí se puede agregar un método alternativo de descarga
        return f"[downloader] Error descargando {url}: {e}"

def hook_progreso(d):
    """
    Hook para mostrar progreso o integrar con future features.
    """
    if d['status'] == 'finished':
        logging.info(f"[downloader] Descarga completada: {d['filename']}")
    elif d['status'] == 'downloading':
        pct = d.get('_percent_str', '0%')
        logging.info(f"[downloader] Descargando {d['filename']}: {pct}")