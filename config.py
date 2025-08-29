"""
config.py - VERSIÓN MEJORADA
Configuración completa de SouaweakBot con validaciones y configuraciones avanzadas.
Estilo Senku: científico, preciso y a prueba de fallos.
"""

import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno desde .env
load_dotenv()

# --- CONFIGURACIÓN DE ENTORNO ---
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# --- TOKEN de Telegram (CRÍTICO) ---
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError(
        "❌ TELEGRAM TOKEN no definido.\n"
        "Crea un archivo .env con: TOKEN=tu_token_aquí\n"
        "Obtén tu token desde @BotFather en Telegram"
    )

# Validar formato básico del token
if not TOKEN.count(":") == 1 or len(TOKEN) < 40:
    raise RuntimeError("❌ TOKEN de Telegram tiene formato inválido")

# --- RUTAS DE CARPETAS ---
BASE_DIR = Path(__file__).parent.absolute()

# Carpetas principales
DOWNLOADS_DIR = BASE_DIR / "downloads"
TEMP_DIR = BASE_DIR / "temp"
LOGS_DIR = BASE_DIR / "logs"

# Subcarpetas de contenido
VIDEOS_DIR = DOWNLOADS_DIR / "videos"
FOTOS_DIR = DOWNLOADS_DIR / "fotos" 
AUDIO_DIR = DOWNLOADS_DIR / "audio"
MANGAS_DIR = DOWNLOADS_DIR / "mangas"
STICKERS_DIR = DOWNLOADS_DIR / "stickers"
QR_TEMP_DIR = TEMP_DIR / "qr_images"
HISTORIAL_DIR = DOWNLOADS_DIR / "historial"

# Lista de todas las carpetas para crear
ALL_DIRECTORIES = [
    DOWNLOADS_DIR, TEMP_DIR, LOGS_DIR,
    VIDEOS_DIR, FOTOS_DIR, AUDIO_DIR, MANGAS_DIR, 
    STICKERS_DIR, QR_TEMP_DIR, HISTORIAL_DIR
]

# Crear carpetas y validar permisos
def _setup_directories():
    """Crea directorios y valida permisos de escritura"""
    for directory in ALL_DIRECTORIES:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            # Test de escritura
            test_file = directory / ".write_test"
            test_file.write_text("test")
            test_file.unlink()  # Eliminar archivo de prueba
        except PermissionError:
            raise RuntimeError(f"❌ Sin permisos de escritura en: {directory}")
        except Exception as e:
            raise RuntimeError(f"❌ Error creando directorio {directory}: {e}")

_setup_directories()

# --- LÍMITES Y CONFIGURACIÓN DE RECURSOS ---
# Límite de almacenamiento
STORAGE_LIMIT_GB = int(os.getenv("STORAGE_LIMIT_GB", "20"))
if STORAGE_LIMIT_GB < 1 or STORAGE_LIMIT_GB > 1000:
    raise ValueError("❌ STORAGE_LIMIT_GB debe estar entre 1 y 1000")

# Límites de descarga
MAX_PARALLEL_DOWNLOADS = int(os.getenv("MAX_PARALLEL_DOWNLOADS", "3"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "2000"))  # 2GB por archivo
CHUNK_SIZE_MB = int(os.getenv("CHUNK_SIZE_MB", "10"))  # Para chunked downloads

# Límites de recursos del sistema
MAX_CPU_PERCENT = int(os.getenv("MAX_CPU_PERCENT", "90"))
MAX_RAM_PERCENT = int(os.getenv("MAX_RAM_PERCENT", "85"))
MIN_FREE_DISK_GB = int(os.getenv("MIN_FREE_DISK_GB", "2"))

# --- CONFIGURACIÓN DE MÓDULOS ---
# YT-DLP
YTDLP_FORMAT = os.getenv("YTDLP_FORMAT", "bestvideo+bestaudio/best")
YTDLP_EXTRACT_FLAT = os.getenv("YTDLP_EXTRACT_FLAT", "False").lower() == "true"

# OCR (Tesseract)
OCR_LANGUAGES = os.getenv("OCR_LANGUAGES", "eng+spa").split("+")
OCR_CONFIG = os.getenv("OCR_CONFIG", "--psm 6")

# Análisis de imágenes
ENABLE_OBJECT_DETECTION = os.getenv("ENABLE_OBJECT_DETECTION", "True").lower() == "true"
ENABLE_NSFW_DETECTION = os.getenv("ENABLE_NSFW_DETECTION", "True").lower() == "true"
ENABLE_METADATA_EXTRACTION = os.getenv("ENABLE_METADATA_EXTRACTION", "True").lower() == "true"

# --- ESTÉTICA Y UI ---
ESTETICA = {
    "color_principal": os.getenv("COLOR_PRINCIPAL", "#1abc9c"),
    "color_secundario": os.getenv("COLOR_SECUNDARIO", "#16a085"),
    "color_error": os.getenv("COLOR_ERROR", "#e74c3c"),
    "color_exito": os.getenv("COLOR_EXITO", "#27ae60"),
    
    # Emojis configurables
    "emoji_inicio": "🚀",
    "emoji_manga": "📚", 
    "emoji_video": "🎬",
    "emoji_audio": "🎵",
    "emoji_historial": "📜",
    "emoji_juego": "🎮",
    "emoji_qr": "🔍",
    "emoji_loading": "⏳",
    "emoji_success": "✅",
    "emoji_error": "❌",
    "emoji_warning": "⚠️",
}

# --- CONFIGURACIÓN DE LOGGING ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = LOGS_DIR / "souaweakbot.log"
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))

# --- CONFIGURACIÓN DE TELEGRAM ---
# Timeouts para requests
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
CONNECT_TIMEOUT = int(os.getenv("CONNECT_TIMEOUT", "10"))

# Configuración de mensajes
MAX_MESSAGE_LENGTH = 4096  # Límite de Telegram
MAX_CAPTION_LENGTH = 1024  # Límite para captions

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Usuarios administradores (IDs de Telegram)
ADMIN_USER_IDS = []
admin_ids_str = os.getenv("ADMIN_USER_IDS", "")
if admin_ids_str:
    try:
        ADMIN_USER_IDS = [int(uid.strip()) for uid in admin_ids_str.split(",")]
    except ValueError:
        print("⚠️ WARNING: ADMIN_USER_IDS tiene formato inválido")

# Rate limiting
ENABLE_RATE_LIMIT = os.getenv("ENABLE_RATE_LIMIT", "True").lower() == "true"
MAX_REQUESTS_PER_MINUTE = int(os.getenv("MAX_REQUESTS_PER_MINUTE", "10"))

# --- CONFIGURACIÓN AVANZADA ---
# Redis para caché (opcional)
REDIS_URL = os.getenv("REDIS_URL", None)
USE_REDIS_CACHE = REDIS_URL is not None

# Base de datos (opcional)
DATABASE_URL = os.getenv("DATABASE_URL", None)
USE_DATABASE = DATABASE_URL is not None

# --- CONFIGURACIÓN DE DESARROLLO ---
if ENVIRONMENT == "development":
    STORAGE_LIMIT_GB = min(STORAGE_LIMIT_GB, 5)  # Límite menor en dev
    MAX_PARALLEL_DOWNLOADS = min(MAX_PARALLEL_DOWNLOADS, 2)
    print("🔧 Ejecutando en modo DESARROLLO")

# --- VALIDACIÓN FINAL ---
def validate_config():
    """Valida toda la configuración al importar el módulo"""
    validations = [
        (STORAGE_LIMIT_GB > 0, "STORAGE_LIMIT_GB debe ser positivo"),
        (MAX_PARALLEL_DOWNLOADS > 0, "MAX_PARALLEL_DOWNLOADS debe ser positivo"),
        (MAX_FILE_SIZE_MB > 0, "MAX_FILE_SIZE_MB debe ser positivo"),
        (0 < MAX_CPU_PERCENT <= 100, "MAX_CPU_PERCENT debe estar entre 1-100"),
        (0 < MAX_RAM_PERCENT <= 100, "MAX_RAM_PERCENT debe estar entre 1-100"),
        (MIN_FREE_DISK_GB > 0, "MIN_FREE_DISK_GB debe ser positivo"),
    ]
    
    for condition, error_msg in validations:
        if not condition:
            raise ValueError(f"❌ {error_msg}")

# Ejecutar validación al importar
validate_config()

# --- INFORMACIÓN DEL SISTEMA ---
def print_config_info():
    """Imprime información de configuración (útil para debugging)"""
    if DEBUG:
        print("=" * 50)
        print("🔧 CONFIGURACIÓN DE SOUAWEAKBOT")
        print(f"📁 Directorio base: {BASE_DIR}")
        print(f"💾 Límite almacenamiento: {STORAGE_LIMIT_GB}GB")
        print(f"⬇️  Descargas paralelas: {MAX_PARALLEL_DOWNLOADS}")
        print(f"🔍 Detección objetos: {ENABLE_OBJECT_DETECTION}")
        print(f"🛡️  Detección NSFW: {ENABLE_NSFW_DETECTION}")
        print(f"👥 Admins: {len(ADMIN_USER_IDS)} usuarios")
        print("=" * 50)

# Solo mostrar info si se ejecuta directamente
if __name__ == "__main__":
    print_config_info()