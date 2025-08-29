# modulos/comandos.py - VERSIÓN COMPLETA
"""
Comandos completos de SouaweakBot.
Incluye todos los comandos mencionados en la estructura.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modulos import historial, kotatsu

# --- Comandos básicos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de inicio con menú interactivo"""
    keyboard = [
        [
            InlineKeyboardButton("📚 Manga/Manhwa", callback_data="kotatsu"),
            InlineKeyboardButton("🎬 Descargar Video", callback_data="downloader")
        ],
        [
            InlineKeyboardButton("🎵 Audio", callback_data="audio"),
            InlineKeyboardButton("📜 Historial", callback_data="historial")
        ],
        [
            InlineKeyboardButton("🎮 Juego", callback_data="game"),
            InlineKeyboardButton("🔍 Analizar QR", callback_data="qr")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensaje_bienvenida = (
        "🚀 **Bienvenido a SouaweakBot v2.0**\n\n"
        "🤖 *El bot más poderoso que jamás verás*\n"
        "👨‍💻 Creado por Kaewaous\n\n"
        "**¿Qué puedo hacer?**\n"
        "• 📚 Descargar mangas/manhwas\n"
        "• 🎬 Descargar videos de cualquier plataforma\n"
        "• 🎵 Extraer audio de videos\n"
        "• 🔍 Analizar códigos QR y texto en imágenes\n"
        "• 👁️ Detectar objetos en imágenes\n"
        "• 📊 Extraer metadatos EXIF/GPS\n"
        "• 🎮 Mini-juegos interactivos\n\n"
        "**Simplemente envía:**\n"
        "• URL para descargar\n"
        "• Imagen para análisis completo\n"
        "• Comando /help para más opciones"
    )
    
    await update.message.reply_text(
        mensaje_bienvenida,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ayuda completa del bot"""
    texto_ayuda = (
        "🔥 **COMANDOS DISPONIBLES:**\n\n"
        "**📋 BÁSICOS:**\n"
        "/start - Iniciar el bot con menú\n"
        "/help - Ver esta ayuda completa\n\n"
        "**📚 CONTENIDO:**\n"
        "/kotatsu - Buscar y descargar mangas\n"
        "/historial - Ver tu historial de descargas\n"
        "/game - Iniciar mini-juegos\n"
        "/qr - Información sobre códigos QR\n\n"
        "**🤖 FUNCIONALIDADES AUTOMÁTICAS:**\n"
        "• Envía cualquier URL → Descarga automática\n"
        "• Envía una imagen → Análisis completo:\n"
        "  ∘ Códigos QR/códigos de barras\n"
        "  ∘ Texto (OCR)\n"
        "  ∘ Objetos detectados\n"
        "  ∘ Metadatos EXIF/GPS\n"
        "  ∘ Análisis de seguridad\n\n"
        "**🎯 PLATAFORMAS SOPORTADAS:**\n"
        "• YouTube (videos/playlists/música)\n"
        "• Instagram (posts/stories/reels)\n"
        "• TikTok (videos/música)\n"
        "• Twitter/X (videos/GIFs)\n"
        "• Facebook (videos públicos)\n"
        "• Y muchas más...\n\n"
        "**💡 TIPS:**\n"
        "• El bot analiza automáticamente el contenido\n"
        "• Historial se guarda por usuario\n"
        "• Archivos se organizan por categoría\n"
        "• Limpieza automática de espacio"
    )
    
    await update.message.reply_text(texto_ayuda, parse_mode='Markdown')

async def kotatsu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando para mangas"""
    keyboard = [
        [
            InlineKeyboardButton("🔍 Buscar Manga", callback_data="manga_search"),
            InlineKeyboardButton("📖 Últimos Capítulos", callback_data="manga_latest")
        ],
        [
            InlineKeyboardButton("⭐ Populares", callback_data="manga_popular"),
            InlineKeyboardButton("🆕 Nuevos", callback_data="manga_new")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensaje = (
        "📚 **KOTATSU - MANGA DOWNLOADER**\n\n"
        "🔥 *Tu fuente definitiva de mangas y manhwas*\n\n"
        "**Funciones disponibles:**\n"
        "• Buscar por nombre\n"
        "• Descargar capítulos individuales\n"
        "• Descargar series completas\n"
        "• Últimos capítulos actualizados\n"
        "• Mangas más populares\n\n"
        "**Ejemplo:** Envía el nombre del manga que buscas"
    )
    
    await update.message.reply_text(
        mensaje,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def historial_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver historial de descargas del usuario"""
    usuario_id = update.message.from_user.id
    
    # Obtener historial del usuario
    registros = historial.ultimo(usuario_id, 10)  # Últimos 10
    
    if not registros:
        await update.message.reply_text(
            "📜 **TU HISTORIAL**\n\n"
            "🤷‍♂️ Aún no tienes descargas registradas.\n"
            "¡Envía una URL o imagen para empezar!"
        )
        return
    
    # Crear mensaje del historial
    mensaje = "📜 **TU HISTORIAL** (últimos 10):\n\n"
    
    for i, registro in enumerate(registros, 1):
        tipo_emoji = {
            "videos": "🎬",
            "audio": "🎵", 
            "fotos": "📷",
            "mangas": "📚",
            "qr": "🔍",
            "ocr": "📝",
            "objetos": "👁️",
            "metadata": "🌍"
        }.get(registro["tipo"], "📄")
        
        mensaje += f"{i}. {tipo_emoji} **{registro['tipo'].upper()}**\n"
        mensaje += f"   📁 {registro['nombre']}\n"
        mensaje += f"   📅 {registro['fecha']}\n"
        
        if registro.get('duracion'):
            mensaje += f"   ⏱️ {registro['duracion']}\n"
        if registro.get('url'):
            mensaje += f"   🔗 {registro['url'][:50]}...\n"
        mensaje += "\n"
    
    # Botones adicionales
    keyboard = [
        [
            InlineKeyboardButton("🗑️ Limpiar Historial", callback_data="clear_history"),
            InlineKeyboardButton("📊 Estadísticas", callback_data="history_stats")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        mensaje,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def game_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mini-juegos interactivos"""
    keyboard = [
        [
            InlineKeyboardButton("🎯 Adivina el Número", callback_data="game_guess"),
            InlineKeyboardButton("🧩 Trivia", callback_data="game_trivia")
        ],
        [
            InlineKeyboardButton("🎲 Dados", callback_data="game_dice"),
            InlineKeyboardButton("🃏 Carta Random", callback_data="game_card")
        ],
        [
            InlineKeyboardButton("🔢 Calculadora", callback_data="game_calc"),
            InlineKeyboardButton("🎪 Sorpréndeme", callback_data="game_random")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    mensaje = (
        "🎮 **MINI-JUEGOS**\n\n"
        "🎯 *Diversión mientras esperas tus descargas*\n\n"
        "**Juegos disponibles:**\n"
        "• 🎯 Adivina el número (1-100)\n"
        "• 🧩 Trivia de cultura general\n"
        "• 🎲 Lanzar dados virtuales\n"
        "• 🃏 Carta aleatoria\n"
        "• 🔢 Calculadora interactiva\n"
        "• 🎪 Sorpresa aleatoria\n\n"
        "¡Elige tu juego favorito!"
    )
    
    await update.message.reply_text(
        mensaje,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre códigos QR"""
    mensaje = (
        "🔍 **ANALIZADOR DE CÓDIGOS QR**\n\n"
        "🤖 *Detección automática inteligente*\n\n"
        "**¿Qué puedo detectar?**\n"
        "• 📶 Códigos WiFi (SSID + contraseña)\n"
        "• 🔗 URLs y enlaces\n"
        "• 📧 Direcciones de email\n"
        "• 📱 Información de contacto\n"
        "• 📝 Texto plano\n"
        "• 📍 Coordenadas GPS\n\n"
        "**¿Cómo usar?**\n"
        "1. Envía una imagen con código QR\n"
        "2. El bot lo analizará automáticamente\n"
        "3. Recibirás toda la información decodificada\n\n"
        "**💡 Tip:** También detecta códigos de barras comunes\n"
        "**🔒 Seguridad:** Todo se procesa localmente"
    )
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')

# --- Comandos de administración (solo para admins) ---
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Estadísticas del bot (solo admin)"""
    # Aquí puedes agregar verificación de admin
    mensaje = (
        "📊 **ESTADÍSTICAS DEL BOT**\n\n"
        "🚧 *En desarrollo...*\n\n"
        "Próximamente mostraré:\n"
        "• Total de usuarios\n"
        "• Descargas por día\n"
        "• Uso de recursos\n"
        "• Módulos más utilizados"
    )
    
    await update.message.reply_text(mensaje, parse_mode='Markdown')