"""
bot.py - VERSIÓN FIX SIMPLE
Solo registra los comandos que SABEMOS que existen.
"""

import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.error import NetworkError, TelegramError

import config
from modulos import comandos, interprete, callback_handlers

# Configuración de logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("souaweakbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja errores globales del bot"""
    logger.error(f"Error causado por update {update}: {context.error}")
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "🔧 Algo salió mal. Intenta de nuevo en un momento."
            )
        except Exception as e:
            logger.error(f"No se pudo enviar mensaje de error: {e}")

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja comandos desconocidos"""
    comando = update.message.text
    await update.message.reply_text(
        f"❌ Comando `{comando}` no reconocido.\n"
        "Usa /help para ver comandos disponibles."
    )

def main():
    try:
        # Verificar configuración
        if not config.TOKEN:
            print("❌ TOKEN no configurado")
            sys.exit(1)
        
        # Crear aplicación
        app = Application.builder().token(config.TOKEN).build()
        
        # === REGISTRAR TODOS LOS COMANDOS ===
        app.add_handler(CommandHandler("start", comandos.start))
        app.add_handler(CommandHandler("help", comandos.help_command))  
        app.add_handler(CommandHandler("kotatsu", comandos.kotatsu_command))
        app.add_handler(CommandHandler("historial", comandos.historial_command))
        app.add_handler(CommandHandler("game", comandos.game_command))
        app.add_handler(CommandHandler("qr", comandos.qr_command))
        app.add_handler(CommandHandler("stats", comandos.stats_command))
        
        # === CALLBACKS (BOTONES) ===
        app.add_handler(CallbackQueryHandler(callback_handlers.handle_callback))
        
        # === MENSAJES ===
        app.add_handler(MessageHandler(
            filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL,
            interprete.interpretar
        ))
        
        # === COMANDOS DESCONOCIDOS ===
        app.add_handler(MessageHandler(filters.COMMAND, unknown_command))
        
        # === ERROR HANDLER ===
        app.add_error_handler(error_handler)
        
        print("=" * 50)
        print("🚀 SouaweakBot v2.0 - LISTO PARA DOMINAR")
        print("👨‍💻 Creado por Kaewaous")
        print("=" * 50)
        
        # Ejecutar
        app.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"❌ Error crítico: {e}")
        print(f"💥 Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Bot detenido por el usuario")

if __name__ == "__main__":
    main()