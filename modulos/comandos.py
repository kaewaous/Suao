# modulos/comandos.py
from telegram import Update
from telegram.ext import ContextTypes

# --- Comandos async ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bienvenido a SouaweakBot v1.0\nEl bot más poderoso que jamás verás."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "Comandos disponibles:\n"
        "/start - Iniciar el bot\n"
        "/help - Ver esta ayuda\n"
        "/kotatsu - Activar Kotatsu (placeholder)\n"
        "/historial - Ver historial (placeholder)\n"
        "/game - Jugar (placeholder)\n"
        "/qr - Generar QR (placeholder)"
    )
    await update.message.reply_text(texto)

async def kotatsu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Kotatsu activado! (placeholder)")

async def historial_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Historial vacío (placeholder)")

async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Juego iniciado (placeholder)")

async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("QR generado (placeholder)")