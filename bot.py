# bot.py
"""
Núcleo de SouaweakBot.
Inicializa todos los handlers y ejecuta el bot de Telegram.
"""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import config
from modulos import comandos, interprete

# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    app = Application.builder().token(config.TOKEN).build()

    # --- Comandos ---
    app.add_handler(CommandHandler("start", comandos.start))
    app.add_handler(CommandHandler("help", comandos.help_command))
    app.add_handler(CommandHandler("kotatsu", comandos.kotatsu_command))

    # --- Mensajes ---
    app.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL,
        interprete.interpretar
    ))

    # Handler para comandos desconocidos
    async def unknown(update, context):
        await update.message.reply_text("❌ Comando no reconocido. Prueba /help.")
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    print("🚀 SouaweakBot ultra-épico corriendo y listo...")
    import asyncio
    asyncio.run(app.run_polling())

if __name__ == "__main__":
    main()