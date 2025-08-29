"""
Menu.py
Menús interactivos de SouaweakBot con soporte para imágenes.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CommandHandler, MessageHandler, filters
from .Botones import menu_principal, botones_confirmacion

# --- Función genérica para mostrar un menú con imagen ---
async def mostrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                       texto: str, botones, imagen_path: str = None):
    """
    Muestra un menú con texto, botones inline y opcionalmente una imagen.

    Args:
        update: Update de Telegram.
        context: Context del handler.
        texto: Texto del menú.
        botones: InlineKeyboardMarkup con botones.
        imagen_path: Ruta de la imagen opcional.
    """
    if imagen_path:
        # Si hay imagen, se envía con caption y botones
        await update.message.reply_photo(
            photo=open(imagen_path, "rb"),
            caption=texto,
            reply_markup=botones
        )
    else:
        # Si no hay imagen, solo texto con botones
        await update.message.reply_text(
            text=texto,
            reply_markup=botones
        )

# --- Menú principal ---
async def mostrar_menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🚀 Bienvenido a SouaweakBot\n"
        "Creado por Kaewaous\n\n"
        "Selecciona una opción para comenzar:\n"
        "• Manga/Manhwa\n"
        "• Descargar Video/Audio\n"
        "• Audio\n"
        "• Historial\n"
        "• Juego Historia\n"
        "• Analizar QR"
    )
    imagen = "estetica/menu_principal.png"  # <-- Slot editable para la imagen
    await mostrar_menu(update, context, texto, menu_principal(), imagen)