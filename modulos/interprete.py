import os
import re
import cv2
from pyzbar.pyzbar import decode
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from modulos import downloader

# Carpeta para imágenes temporales
CARPETA_IMAGENES = "imagenes_qr"
os.makedirs(CARPETA_IMAGENES, exist_ok=True)

async def interpretar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message
    usuario_id = mensaje.from_user.id

    # --- Si manda texto ---
    if mensaje.text:
        urls = re.findall(r'https?://\S+', mensaje.text)
        if urls:
            for url in urls:
                await mensaje.reply_text(f"🔄 Descargando video desde: {url}")
                resultado = downloader.descargar(url, usuario_id)
                
                # Enviar video si es tipo video
                if resultado.get("categoria") == "videos":
                    ruta_video = resultado.get("archivo_path")
                    if os.path.exists(ruta_video):
                        try:
                            await context.bot.send_video(chat_id=update.effective_chat.id,
                                                         video=InputFile(ruta_video))
                        except Exception as e:
                            await mensaje.reply_text(f"❌ Error enviando video: {e}")
                    else:
                        await mensaje.reply_text("❌ El video no se encontró después de descargarlo.")
                else:
                    await mensaje.reply_text(f"[downloader] {resultado.get('categoria').capitalize()} descargado: {resultado.get('titulo')}")
            return
        else:
            await mensaje.reply_text(f"[Asistente] Recibí tu mensaje: {mensaje.text}")
            return

    # --- Si manda foto ---
    if mensaje.photo:
        foto = mensaje.photo[-1]  # Mejor calidad
        file = await foto.get_file()
        ruta_local = os.path.join(CARPETA_IMAGENES, f"{usuario_id}_qr.jpg")
        await file.download_to_drive(ruta_local)

        qr_info = decodificar_qr(ruta_local)
        if qr_info:
            await mensaje.reply_text(f"📷 Código QR detectado:\n{qr_info}")
        else:
            await mensaje.reply_text("📷 Recibí tu imagen, pero no encontré ningún QR.")
        return

    # --- Otros tipos de archivo ---
    await mensaje.reply_text("⚠️ Aún no sé interpretar ese tipo de archivo.")

def decodificar_qr(ruta_imagen: str) -> str | None:
    """Intenta leer códigos QR de la imagen usando pyzbar y OpenCV."""
    try:
        img = cv2.imread(ruta_imagen)
        if img is None:
            return None

        datos_qr = decode(img)
        if not datos_qr:
            return None

        return "\n".join([qr.data.decode("utf-8") for qr in datos_qr])

    except Exception as e:
        print(f"Error al decodificar QR: {e}")
        return None