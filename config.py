# config.py
"""
Configuración de SouaweakBot.
Incluye token, rutas, límites de almacenamiento y opciones de estética.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- TOKEN de Telegram ---
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TELEGRAM TOKEN no definido. Revisa tu archivo .env")

# --- Rutas de carpetas ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
VIDEOS_DIR = os.path.join(DOWNLOADS_DIR, "videos")
FOTOS_DIR = os.path.join(DOWNLOADS_DIR, "fotos")
AUDIO_DIR = os.path.join(DOWNLOADS_DIR, "audio")
MANGAS_DIR = os.path.join(DOWNLOADS_DIR, "mangas")

# Crear carpetas si no existen
for path in [DOWNLOADS_DIR, VIDEOS_DIR, FOTOS_DIR, AUDIO_DIR, MANGAS_DIR]:
    os.makedirs(path, exist_ok=True)

# --- Límite de almacenamiento (GB) ---
STORAGE_LIMIT_GB = 20

# --- Opciones de estética para menús y botones ---
ESTETICA = {
    "color_principal": "#1abc9c",
    "color_secundario": "#16a085",
    "emoji_inicio": "🚀",
    "emoji_manga": "📚",
    "emoji_video": "🎬",
    "emoji_audio": "🎵",
    "emoji_historial": "📜",
    "emoji_juego": "🎮",
    "emoji_qr": "🔗",
}

# --- Opciones adicionales ---
MAX_PARALLEL_DOWNLOADS = 3