"""
callback_handlers.py
Maneja todos los callbacks de botones inline del bot.
Estilo L: cada callback tiene su lógica específica.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from modulos import historial, kotatsu
import random

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Router principal para todos los callbacks de botones.
    """
    query = update.callback_query
    await query.answer()  # Confirmar que se recibió el callback
    
    data = query.data
    
    # === MENÚ PRINCIPAL ===
    if data == "kotatsu":
        await callback_kotatsu(update, context)
    elif data == "downloader":
        await callback_downloader(update, context)
    elif data == "audio":
        await callback_audio(update, context)
    elif data == "historial":
        await callback_historial(update, context)
    elif data == "game":
        await callback_game(update, context)
    elif data == "qr":
        await callback_qr(update, context)
    
    # === MANGA CALLBACKS ===
    elif data == "manga_search":
        await callback_manga_search(update, context)
    elif data == "manga_latest":
        await callback_manga_latest(update, context)
    elif data == "manga_popular":
        await callback_manga_popular(update, context)
    elif data == "manga_new":
        await callback_manga_new(update, context)
    
    # === HISTORIAL CALLBACKS ===
    elif data == "clear_history":
        await callback_clear_history(update, context)
    elif data == "history_stats":
        await callback_history_stats(update, context)
    
    # === JUEGOS CALLBACKS ===
    elif data == "game_guess":
        await callback_game_guess(update, context)
    elif data == "game_trivia":
        await callback_game_trivia(update, context)
    elif data == "game_dice":
        await callback_game_dice(update, context)
    elif data == "game_card":
        await callback_game_card(update, context)
    elif data == "game_calc":
        await callback_game_calc(update, context)
    elif data == "game_random":
        await callback_game_random(update, context)
    
    else:
        await query.edit_message_text("❓ Opción no implementada aún")

# === CALLBACKS DEL MENÚ PRINCIPAL ===

async def callback_kotatsu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Submenu de Kotatsu/Manga"""
    keyboard = [
        [
            InlineKeyboardButton("🔍 Buscar Manga", callback_data="manga_search"),
            InlineKeyboardButton("📖 Últimos Capítulos", callback_data="manga_latest")
        ],
        [
            InlineKeyboardButton("⭐ Populares", callback_data="manga_popular"),
            InlineKeyboardButton("🆕 Nuevos", callback_data="manga_new")
        ],
        [InlineKeyboardButton("🔙 Volver", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    texto = (
        "📚 **KOTATSU - MANGA DOWNLOADER**\n\n"
        "🔥 *Tu fuente definitiva de mangas y manhwas*\n\n"
        "**Funciones disponibles:**\n"
        "• Buscar por nombre\n"
        "• Descargar capítulos individuales\n"
        "• Descargar series completas\n"
        "• Últimos capítulos actualizados\n"
        "• Mangas más populares\n\n"
        "**📝 Tip:** También puedes enviar directamente el nombre del manga"
    )
    
    await update.callback_query.edit_message_text(
        texto, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def callback_downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre el downloader"""
    texto = (
        "🎬 **DESCARGADOR UNIVERSAL**\n\n"
        "🌐 *Compatible con +1000 sitios*\n\n"
        "**Plataformas soportadas:**\n"
        "• YouTube (videos/playlists/música)\n"
        "• Instagram (posts/stories/reels)\n"
        "• TikTok (videos/música)\n"
        "• Twitter/X (videos/GIFs)\n"
        "• Facebook (videos públicos)\n"
        "• Twitch (clips/VODs)\n"
        "• Reddit (videos/GIFs)\n"
        "• Y muchas más...\n\n"
        "**💡 Cómo usar:**\n"
        "1. Copia la URL del video\n"
        "2. Pégala en el chat\n"
        "3. ¡El bot hará el resto!\n\n"
        "**🎯 Formatos:** MP4, WebM, MP3, M4A"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        texto,
        parse_mode='Markdown', 
        reply_markup=reply_markup
    )

async def callback_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre extracción de audio"""
    texto = (
        "🎵 **EXTRACTOR DE AUDIO**\n\n"
        "🎶 *Audio de alta calidad desde cualquier video*\n\n"
        "**Funcionalidades:**\n"
        "• Extrae audio de videos\n"
        "• Formatos: MP3, M4A, WAV\n"
        "• Calidad hasta 320kbps\n"
        "• Metadatos automáticos\n"
        "• Compatible con playlists\n\n"
        "**💡 Uso:**\n"
        "• Envía URL de video\n"
        "• El bot detecta automáticamente\n"
        "• Recibes el audio extraído\n\n"
        "**🎯 Perfecto para:** Música, podcasts, conferencias"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def callback_historial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostrar historial del usuario"""
    usuario_id = update.callback_query.from_user.id
    registros = historial.ultimo(usuario_id, 5)
    
    if not registros:
        texto = (
            "📜 **TU HISTORIAL**\n\n"
            "🤷‍♂️ Aún no tienes descargas registradas.\n"
            "¡Envía una URL o imagen para empezar!"
        )
        keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_main")]]
    else:
        texto = "📜 **TU HISTORIAL** (últimos 5):\n\n"
        for i, registro in enumerate(registros, 1):
            tipo_emoji = {
                "videos": "🎬", "audio": "🎵", "fotos": "📷",
                "mangas": "📚", "qr": "🔍"
            }.get(registro["tipo"], "📄")
            
            texto += f"{i}. {tipo_emoji} {registro['nombre'][:30]}...\n"
            texto += f"   📅 {registro['fecha']}\n\n"
        
        keyboard = [
            [
                InlineKeyboardButton("🗑️ Limpiar", callback_data="clear_history"),
                InlineKeyboardButton("📊 Estadísticas", callback_data="history_stats")
            ],
            [InlineKeyboardButton("🔙 Volver", callback_data="back_main")]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def callback_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Submenu de juegos"""
    keyboard = [
        [
            InlineKeyboardButton("🎯 Adivina Número", callback_data="game_guess"),
            InlineKeyboardButton("🧩 Trivia", callback_data="game_trivia")
        ],
        [
            InlineKeyboardButton("🎲 Dados", callback_data="game_dice"),
            InlineKeyboardButton("🃏 Carta Random", callback_data="game_card")
        ],
        [
            InlineKeyboardButton("🔢 Calculadora", callback_data="game_calc"),
            InlineKeyboardButton("🎪 Sorpréndeme", callback_data="game_random")
        ],
        [InlineKeyboardButton("🔙 Volver", callback_data="back_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    texto = (
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
    
    await update.callback_query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def callback_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre análisis QR"""
    texto = (
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
        "**💡 Tip:** También detecta códigos de barras"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="back_main")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        texto,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# === CALLBACKS DE JUEGOS ===

async def callback_game_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Juego de dados"""
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    total = dado1 + dado2
    
    dados_emoji = ["", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    
    resultado = (
        f"🎲 **LANZAMIENTO DE DADOS**\n\n"
        f"Dado 1: {dados_emoji[dado1]} ({dado1})\n"
        f"Dado 2: {dados_emoji[dado2]} ({dado2})\n\n"
        f"**Total: {total}**\n\n"
    )
    
    if total == 12:
        resultado += "🎉 ¡DOBLE SEIS! ¡Increíble!"
    elif total == 2:
        resultado += "😅 Doble uno... ¡Mejor suerte la próxima!"
    elif total >= 10:
        resultado += "🔥 ¡Excelente tirada!"
    elif total <= 4:
        resultado += "😬 Tirada baja, ¡inténtalo de nuevo!"
    
    keyboard = [
        [InlineKeyboardButton("🎲 Lanzar de Nuevo", callback_data="game_dice")],
        [InlineKeyboardButton("🔙 Volver a Juegos", callback_data="game")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        resultado,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def callback_game_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Carta aleatoria"""
    palos = ["♠️", "♥️", "♦️", "♣️"]
    valores = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    palo = random.choice(palos)
    valor = random.choice(valores)
    
    # Nombres de palos
    nombre_palo = {"♠️": "Picas", "♥️": "Corazones", "♦️": "Diamantes", "♣️": "Tréboles"}[palo]
    
    resultado = (
        f"🃏 **CARTA ALEATORIA**\n\n"
        f"Tu carta es:\n"
        f"**{valor} de {nombre_palo} {palo}**\n\n"
    )
    
    # Significados especiales
    if valor == "A":
        resultado += "🎯 ¡As! La carta más poderosa."
    elif valor in ["J", "Q", "K"]:
        resultado += "👑 ¡Figura real! Una carta noble."
    elif valor == "7":
        resultado += "🍀 ¡Siete de la suerte!"
    
    keyboard = [
        [InlineKeyboardButton("🃏 Nueva Carta", callback_data="game_card")],
        [InlineKeyboardButton("🔙 Volver a Juegos", callback_data="game")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        resultado,
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Placeholder para otros callbacks
async def callback_manga_search(update, context):
    await update.callback_query.edit_message_text("🔍 Función de búsqueda en desarrollo...")

async def callback_manga_latest(update, context):
    await update.callback_query.edit_message_text("📖 Últimos capítulos en desarrollo...")

async def callback_manga_popular(update, context):
    await update.callback_query.edit_message_text("⭐ Populares en desarrollo...")

async def callback_manga_new(update, context):
    await update.callback_query.edit_message_text("🆕 Nuevos en desarrollo...")

async def callback_clear_history(update, context):
    await update.callback_query.edit_message_text("🗑️ Función de limpieza en desarrollo...")

async def callback_history_stats(update, context):
    await update.callback_query.edit_message_text("📊 Estadísticas en desarrollo...")

async def callback_game_guess(update, context):
    await update.callback_query.edit_message_text("🎯 Juego de adivinanza en desarrollo...")

async def callback_game_trivia(update, context):
    await update.callback_query.edit_message_text("🧩 Trivia en desarrollo...")

async def callback_game_calc(update, context):
    await update.callback_query.edit_message_text("🔢 Calculadora en desarrollo...")

async def callback_game_random(update, context):
    sorpresas = [
        "🎉 ¡Sorpresa! Tu número de la suerte es: " + str(random.randint(1, 100)),
        "🔮 Predicción: Hoy será un gran día para descargar videos",
        "🎈 Dato curioso: Los pingüinos pueden saltar hasta 2 metros de altura",
        "🌟 Tu color de la suerte hoy es: " + random.choice(["Azul", "Rojo", "Verde", "Morado", "Dorado"]),
        "🎪 ¡Abracadabra! *hace aparecer un emoji mágico* ✨"
    ]
    
    sorpresa = random.choice(sorpresas)
    keyboard = [
        [InlineKeyboardButton("🎪 Otra Sorpresa", callback_data="game_random")],
        [InlineKeyboardButton("🔙 Volver a Juegos", callback_data="game")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.edit_message_text(
        sorpresa,
        reply_markup=reply_markup
    )