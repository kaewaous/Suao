import os
import logging
import subprocess
from modulos import chunked_downloader
import yt_dlp

logger = logging.getLogger(__name__)

# ----------------------------
# Función principal de descarga
# ----------------------------
def descargar(url, ydl_opts):
    """
    Descarga un video usando yt-dlp, con opción a multi-threading/parallel.
    Si falla, recurre al chunked downloader.
    """
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                raise ValueError("No se pudo extraer información del video.")
            archivo_descargado = ydl.prepare_filename(info)
        return archivo_descargado

    except Exception as e:
        logger.warning(f"[parallel_downloader] Descarga falló, intentando chunked: {str(e)}")
        return chunked_downloader.descargar(url, ydl_opts)

# ----------------------------
# Extraer audio de un video
# ----------------------------
def extraer_audio(video_path, audio_path):
    """
    Extrae el audio de un video usando ffmpeg.
    """
    try:
        comando = [
            "ffmpeg", "-y", "-i", video_path,
            "-vn", "-acodec", "libmp3lame", "-q:a", "2",
            audio_path
        ]
        subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"[parallel_downloader] Audio extraído: {audio_path}")
    except Exception as e:
        logger.error(f"[parallel_downloader] Error extrayendo audio: {str(e)}")

# ----------------------------
# Extraer una foto/miniatura del video
# ----------------------------
def extraer_foto(video_path, foto_path, tiempo="00:00:01"):
    """
    Extrae un fotograma del video como miniatura usando ffmpeg.
    Por defecto toma el segundo 1 del video.
    """
    try:
        comando = [
            "ffmpeg", "-y", "-i", video_path,
            "-ss", tiempo, "-vframes", "1", foto_path
        ]
        subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"[parallel_downloader] Foto extraída: {foto_path}")
    except Exception as e:
        logger.error(f"[parallel_downloader] Error extrayendo foto: {str(e)}")