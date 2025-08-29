"""
downloader.py
Descarga total de contenido multimedia de cualquier red social.
Integración con storage_manager, historial, chunked_downloader, parallel_downloader y compressor.
"""

import os
import logging
import re
from modulos import historial, storage_manager
from modulos import chunked_downloader, parallel_downloader, compressor
import yt_dlp

# Configurar logging para errores
logger = logging.getLogger(__name__)

def descargar(url: str, usuario_id: int):
    """
    Descarga cualquier URL de red social y guarda archivo en la carpeta correspondiente.
    Detecta tipo de contenido y registra en historial.
    """
    try:
        # Detectar y limpiar URLs de TikTok
        url = limpiar_url_tiktok(url)
        
        # Configuración avanzada de yt-dlp con opciones específicas
        ydl_opts = {
            'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [hook_progreso],
            'extractor_args': {
                'tiktok': {
                    'format': 'download_addr',
                    'webpage_url': False
                }
            },
            # Headers para evitar bloqueos
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
        }

        info = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if not info:
                return f"[downloader] Error: No se pudo extraer información de {url}"

        # Obtener información del archivo descargado
        filename = ydl.prepare_filename(info)
        ext = info.get('ext', 'mp4')
        titulo = info.get('title', 'archivo_desconocido').replace('/', '_').replace('\\', '_')
        duracion = info.get('duration', 0)

        # Detectar tipo de contenido
        if ext in ['mp4', 'mkv', 'webm', 'mov', 'avi']:
            categoria = "videos"
        elif ext in ['mp3', 'm4a', 'wav', 'ogg', 'flac']:
            categoria = "audio"
        elif ext in ['jpg', 'png', 'jpeg', 'gif', 'webp', 'bmp']:
            categoria = "fotos"
        else:
            categoria = "otros"

        # Ruta completa del archivo
        archivo_path = os.path.join('downloads', f"{titulo}.{ext}")

        # Verificar que el archivo existe antes de guardar
        if not os.path.exists(archivo_path):
            # Buscar el archivo real (yt-dlp a veces cambia extensiones)
            for file in os.listdir('downloads'):
                if file.startswith(titulo):
                    archivo_path = os.path.join('downloads', file)
                    break

        if os.path.exists(archivo_path):
            # Guardar archivo en storage_manager
            storage_manager.guardar_archivo(archivo_path, categoria)

            # Registrar en historial
            historial.registrar(usuario_id, titulo, tipo=categoria, url=url, duracion=duracion)

            return {
                'status': 'success',
                'message': f"[downloader] {categoria.capitalize()} descargado: {titulo}",
                'file_path': archivo_path,
                'file_type': categoria
            }
        else:
            return {
                'status': 'error',
                'message': f"[downloader] Archivo no encontrado después de descargar: {titulo}"
            }

    except yt_dlp.utils.DownloadError as e:
        error_msg = f"[downloader] Error de descarga: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}
        
    except Exception as e:
        error_msg = f"[downloader] Error inesperado con {url}: {str(e)}"
        logger.error(error_msg)
        return {'status': 'error', 'message': error_msg}

def limpiar_url_tiktok(url: str) -> str:
    """
    Limpia y normaliza URLs de TikTok para yt-dlp
    """
    # Patrones de URLs problemáticas de TikTok
    tiktok_patterns = [
        r'https?://vm\.tiktok\.com/[\w]+/',
        r'https?://www\.tiktok\.com/@[\w]+/photo/\d+',
        r'https?://www\.tiktok\.com/t/[\w]+/'
    ]
    
    # Si es una URL de TikTok problemática, usar extractor especial
    for pattern in tiktok_patterns:
        if re.match(pattern, url):
            logger.info(f"URL de TikTok detectada y limpiada: {url}")
            # Forzar el uso del extractor de TikTok
            return url.split('?')[0]  # Remover parámetros de query
    
    return url

def hook_progreso(d):
    """
    Hook para mostrar progreso de descarga
    """
    if d['status'] == 'finished':
        logger.info(f"[downloader] Descarga completada: {d.get('filename', 'unknown')}")
    elif d['status'] == 'downloading':
        filename = os.path.basename(d.get('filename', 'unknown'))
        percent = d.get('_percent_str', '0%')
        speed = d.get('_speed_str', 'N/A')
        logger.info(f"[downloader] {filename}: {percent} a {speed}")