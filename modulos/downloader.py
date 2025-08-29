"""
downloader.py
Descarga total de contenido multimedia de cualquier red social.
Integra storage_manager, historial, chunked_downloader, parallel_downloader y compressor.
Los archivos se guardan en subcarpetas específicas dentro de 'downloads/'.
"""

import os
import logging
import re
import unicodedata
from modulos import historial, storage_manager
from modulos import chunked_downloader, parallel_downloader, compressor
import yt_dlp

logger = logging.getLogger(__name__)

# Rutas base para cada tipo
RUTAS = {
    "videos": "downloads/videos",
    "audio": "downloads/audio",
    "fotos": "downloads/fotos",
    "mangas": "downloads/mangas",
    "otros": "downloads/otros"
}

# Asegurarse que las carpetas existan
for ruta in RUTAS.values():
    os.makedirs(ruta, exist_ok=True)


def nombre_seguro(nombre_original: str) -> str:
    """
    Convierte un nombre de archivo a un formato seguro:
    - Normaliza acentos
    - Reemplaza caracteres no permitidos por "_"
    """
    nombre = unicodedata.normalize('NFKD', nombre_original).encode('ascii', 'ignore').decode('ascii')
    nombre = re.sub(r'[^\w.-]', '_', nombre)
    return nombre


def limpiar_url_tiktok(url: str) -> str:
    """
    Limpia y normaliza URLs de TikTok para yt-dlp
    """
    tiktok_patterns = [
        r'https?://vm\.tiktok\.com/[\w]+/',
        r'https?://www\.tiktok\.com/@[\w]+/photo/\d+',
        r'https?://www\.tiktok\.com/t/[\w]+/'
    ]
    for pattern in tiktok_patterns:
        if re.match(pattern, url):
            logger.info(f"URL de TikTok detectada y limpiada: {url}")
            return url.split('?')[0]
    return url


def hook_progreso(d):
    if d['status'] == 'finished':
        logger.info(f"[downloader] Descarga completada: {d.get('filename', 'unknown')}")
    elif d['status'] == 'downloading':
        filename = os.path.basename(d.get('filename', 'unknown'))
        percent = d.get('_percent_str', '0%')
        speed = d.get('_speed_str', 'N/A')
        logger.info(f"[downloader] {filename}: {percent} a {speed}")


def detectar_categoria(ext: str) -> str:
    """
    Detecta la categoría del archivo según la extensión
    """
    ext = ext.lower()
    if ext in ['mp4', 'mkv', 'webm', 'mov', 'avi']:
        return "videos"
    elif ext in ['mp3', 'm4a', 'wav', 'ogg', 'flac']:
        return "audio"
    elif ext in ['jpg', 'png', 'jpeg', 'gif', 'webp', 'bmp']:
        return "fotos"
    else:
        return "otros"


def descargar(url: str, usuario_id: int):
    """
    Descarga cualquier URL y mueve el archivo a su subcarpeta correspondiente.
    """
    try:
        url = limpiar_url_tiktok(url)

        ydl_opts = {
            'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [hook_progreso],
            'extractor_args': {
                'tiktok': {'format': 'download_addr', 'webpage_url': False}
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
        }

        info = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if not info:
                return {"status": "error", "message": f"[downloader] No se pudo extraer información de {url}"}
            archivo_descargado = ydl.prepare_filename(info)

        # Nombre seguro
        titulo = info.get('title', 'archivo_desconocido')
        nombre_final = nombre_seguro(titulo)
        ext = os.path.splitext(archivo_descargado)[1].lstrip('.')
        categoria = detectar_categoria(ext)
        ruta_destino = os.path.join(RUTAS[categoria], f"{nombre_final}.{ext}")

        # Renombrar/mover archivo
        if archivo_descargado != ruta_destino:
            os.rename(archivo_descargado, ruta_destino)

        # Guardar en storage_manager
        storage_manager.guardar_archivo(ruta_destino, categoria)

        # Registrar historial
        duracion = info.get('duration', 0)
        historial.registrar(usuario_id, titulo, tipo=categoria, url=url, duracion=duracion)

        return {
            'status': 'success',
            'message': f"[downloader] {categoria.capitalize()} descargado: {titulo}",
            'file_path': ruta_destino,
            'file_type': categoria
        }

    except yt_dlp.utils.DownloadError as e:
        error_msg = f"[downloader] Error de descarga: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}

    except Exception as e:
        error_msg = f"[downloader] Error inesperado con {url}: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}
