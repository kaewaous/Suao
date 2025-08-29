import os
import re
import unicodedata
import logging
from modulos import historial, storage_manager
from modulos import chunked_downloader
from modulos import parallel_downloader
import yt_dlp

logger = logging.getLogger(__name__)

# Rutas base
RUTAS = {
    "videos": "downloads/videos",
    "audio": "downloads/audio",
    "fotos": "downloads/fotos",
    "otros": "downloads/otros"
}
for ruta in RUTAS.values():
    os.makedirs(ruta, exist_ok=True)

# Tamaño máximo para descarga normal antes de usar chunked (en bytes)
MAX_SIZE_NORMAL = 50 * 1024 * 1024  # 50 MB

def nombre_seguro(nombre_original: str) -> str:
    nombre = unicodedata.normalize('NFKD', nombre_original).encode('ascii', 'ignore').decode('ascii')
    nombre = re.sub(r'[^\w.-]', '_', nombre)
    return nombre

def detectar_categoria(ext: str) -> str:
    ext = ext.lower()
    if ext in ['mp4', 'mkv', 'webm', 'mov', 'avi']:
        return "videos"
    elif ext in ['mp3', 'm4a', 'wav', 'ogg', 'flac']:
        return "audio"
    elif ext in ['jpg', 'png', 'jpeg', 'gif', 'webp', 'bmp']:
        return "fotos"
    else:
        return "otros"

def hook_progreso(d):
    if d['status'] == 'finished':
        logger.info(f"[downloader] Descarga completada: {d.get('filename', 'unknown')}")
    elif d['status'] == 'downloading':
        filename = os.path.basename(d.get('filename', 'unknown'))
        percent = d.get('_percent_str', '0%')
        speed = d.get('_speed_str', 'N/A')
        logger.info(f"[downloader] {filename}: {percent} a {speed}")

def limpiar_url_tiktok(url: str) -> str:
    tiktok_patterns = [
        r'https?://vm\.tiktok\.com/[\w]+/',
        r'https?://www\.tiktok\.com/@[\w]+/video/\d+',
        r'https?://www\.tiktok\.com/t/[\w]+/'
    ]
    for pattern in tiktok_patterns:
        if re.match(pattern, url):
            logger.info(f"URL de TikTok detectada y limpiada: {url}")
            return url.split('?')[0]
    return url

def descargar(url: str, usuario_id: int):
    """Descarga videos, audio o fotos de cualquier red social, usando chunked si es grande."""
    try:
        url = limpiar_url_tiktok(url)

        ydl_opts = {
            'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s'),
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [hook_progreso],
            'http_headers': {'User-Agent': 'Mozilla/5.0'}
        }

        # Primero extraemos info para tamaño y metadata
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return {"status": "error", "message": "No se pudo extraer información."}
            tamaño_est = info.get('filesize') or info.get('filesize_approx', 0)

        # Usar chunked si es muy grande
        if tamaño_est > MAX_SIZE_NORMAL:
            logger.info(f"[downloader] Video muy grande, usando chunked downloader.")
            archivo_descargado = chunked_downloader.descargar(url, ydl_opts)
        else:
            # Descarga normal con soporte paralelo si se desea
            archivo_descargado = parallel_downloader.descargar(url, ydl_opts)

        # Saneamiento de nombre
        titulo = info.get('title', 'archivo_desconocido')
        nombre_final = nombre_seguro(titulo)
        ext = os.path.splitext(archivo_descargado)[1].lstrip('.')
        categoria = detectar_categoria(ext)
        ruta_destino = os.path.join(RUTAS[categoria], f"{nombre_final}.{ext}")

        if archivo_descargado != ruta_destino:
            os.rename(archivo_descargado, ruta_destino)

        # Guardar en storage y historial
        storage_manager.guardar_archivo(ruta_destino, categoria)
        historial.registrar(usuario_id, titulo, tipo=categoria, url=url, duracion=info.get('duration', 0))

        # Extraer audio o fotos si es video
        if categoria == "videos":
            audio_path = os.path.join(RUTAS['audio'], f"{nombre_final}.mp3")
            parallel_downloader.extraer_audio(ruta_destino, audio_path)
            # Opcional: extraer fotogramas / miniaturas
            foto_path = os.path.join(RUTAS['fotos'], f"{nombre_final}.jpg")
            parallel_downloader.extraer_foto(ruta_destino, foto_path)

        return {
            'status': 'success',
            'message': f"{categoria.capitalize()} descargado: {titulo}",
            'file_path': ruta_destino,
            'file_type': categoria
        }

    except yt_dlp.utils.DownloadError as e:
        logger.error(f"[downloader] Error de descarga: {str(e)}")
        return {'status': 'error', 'message': str(e)}
    except Exception as e:
        logger.error(f"[downloader] Error inesperado con {url}: {str(e)}")
        return {'status': 'error', 'message': str(e)}