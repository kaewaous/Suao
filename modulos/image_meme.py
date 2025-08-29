# modulos/image_meme.py

import os
import io
from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes
from modulos import historial, interprete

# Carpetas para stickers
STICKERS_PATH = "downloads/stickers"
WHATSAPP_PATH = "downloads/whatsapp_stickers"
os.makedirs(STICKERS_PATH, exist_ok=True)
os.makedirs(WHATSAPP_PATH, exist_ok=True)

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Comando /meme para generar un sticker desde una imagen enviada
    Funciona con fotos o documentos de tipo imagen.
    """
    file = None
    # Detectar imagen enviada
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
    elif update.message.document and update.message.document.mime_type.startswith("image/"):
        file = await update.message.document.get_file()

    if not file:
        await update.message.reply_text("Envía una imagen para crear un sticker.")
        return

    # Descargar imagen en memoria
    file_bytes = io.BytesIO()
    await file.download_to_memory(out=file_bytes)
    file_bytes.seek(0)

    # Crear sticker
    sticker_path, whatsapp_path = generar_sticker(file_bytes, update.message.from_user.id)

    # Responder en Telegram
    await update.message.reply_sticker(sticker_path)
    await update.message.reply_text(f"Sticker listo para WhatsApp: {whatsapp_path}")

def generar_sticker(file_bytes: io.BytesIO, user_id: int):
    """
    Función que procesa los bytes de imagen, genera stickers para Telegram y WhatsApp
    Devuelve paths de los archivos
    """
    img = Image.open(file_bytes).convert("RGBA")
    img.thumbnail((512, 512))

    # Sticker para Telegram
    sticker_path = os.path.join(STICKERS_PATH, f"{user_id}_{os.urandom(4).hex()}.webp")
    img.save(sticker_path, format="WEBP")

    # Sticker para WhatsApp
    whatsapp_path = os.path.join(WHATSAPP_PATH, os.path.basename(sticker_path))
    img.save(whatsapp_path, format="WEBP")

    # Guardar en historial
    historial.guardar_historial(user_id, f"Sticker generado: {sticker_path}")

    return sticker_path, whatsapp_path

async def detectar_meme_automatico(file_bytes: bytes, user_id: int):
    """
    Función para integración futura de detección automática de memes
    Genera sticker automáticamente sin comando
    """
    return generar_sticker(io.BytesIO(file_bytes), user_id)