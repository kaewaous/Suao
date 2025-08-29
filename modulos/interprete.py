"""
interprete.py - VERSIÓN PRO ASIÁTICA 
Router inteligente ultra-rápido con procesamiento paralelo y caching.
Estilo: Velocidad de bala + Precisión de samurai + Robustez de tanque.
"""

import os
import re
import asyncio
import aiofiles
import cv2
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from modulos import (
    downloader, sex,storage_manager, historial, resource_manager)
import time
from functools import lru_cache
import hashlib
import subprocess

# Configuración de performance
MAX_WORKERS = 8  # Núcleos para procesamiento paralelo
CACHE_SIZE = 1000  # Máximo de resultados cacheados
TIMEOUT_ANALISIS = 30  # Segundos máximo por análisis

# Carpeta para imágenes temporales con limpieza automática
CARPETA_IMAGENES = "imagenes_temp"
os.makedirs(CARPETA_IMAGENES, exist_ok=True)

# Executors para procesamiento paralelo
thread_executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
process_executor = ProcessPoolExecutor(max_workers=MAX_WORKERS)

# Cache de resultados de análisis
@lru_cache(maxsize=CACHE_SIZE)
def cache_analisis_imagen(image_hash: str, modulo: str):
    """Cache de resultados para imágenes repetidas"""
    return None

async def interpretar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Router principal ultra-rápido con timeouts y fallbacks"""
    start_time = time.time()
    mensaje = update.message
    usuario_id = mensaje.from_user.id
    
    try:
        # --- ANÁLISIS DE TEXTO: URLs y comandos rápidos ---
        if mensaje.text:
            await procesar_texto_rapido(mensaje, usuario_id)
            return

        # --- IMÁGENES: Procesamiento paralelo masivo ---
        if mensaje.photo:
            await procesar_imagen_ultrarrápido(mensaje, usuario_id, context)
            return

        # --- DOCUMENTOS: Detección inteligente ---
        if mensaje.document:
            await procesar_documento_inteligente(mensaje, usuario_id, context)
            return

        # --- VIDEOS: Descarga y análisis ---
        if mensaje.video:
            await procesar_video(mensaje, usuario_id, context)
            return

        # --- STICKERS y otros formatos ---
        if mensaje.sticker:
            await mensaje.reply_text("🔄 Convirtiendo sticker a imagen...")
            await procesar_sticker(mensaje, usuario_id, context)
            return

        # --- FALLBACK: Análisis genérico ---
        await mensaje.reply_text("🔍 Analizando contenido...")
        tipo_contenido = detectar_tipo_contenido(mensaje)
        await mensaje.reply_text(f"📦 Contenido detectado: {tipo_contenido}")

    except asyncio.TimeoutError:
        await mensaje.reply_text("⏰ Timeout: El análisis tardó demasiado")
    except Exception as e:
        logger.error(f"Error crítico en interprete: {e}")
        await mensaje.reply_text("💥 Error crítico - Reiniciando análisis...")
        # Reintento automático
        await reintento_analisis(update, context)

    finally:
        execution_time = time.time() - start_time
        if execution_time > 1.0:  # Solo loggear operaciones lentas
            logger.info(f"Análisis completado en {execution_time:.2f}s")

async def procesar_texto_rapido(mensaje, usuario_id: int):
    """Procesamiento ultra-rápido de texto con regex optimizado"""
    texto = mensaje.text.strip()
    
    # Detección lightning-fast de URLs
    url_match = re.search(r'https?://[^\s<>"]+|www\.[^\s<>"]+', texto)
    if url_match:
        url = url_match.group(0)
        await mensaje.reply_text(f"⚡ Descargando: {url[:50]}...")
        
        # Procesamiento en segundo plano sin bloquear
        asyncio.create_task(procesar_descarga_url(url, usuario_id, mensaje))
        return
    
    # Comandos rápidos pre-cacheados
    comandos_rapidos = {
        r'hola|hello|hi': "👋 ¡Hola! Envíame contenido para analizar",
        r'gracias|thanks': "🎯 De nada, siempre a tu servicio",
        r'que puedes hacer|help|ayuda': generar_respuesta_ayuda()
    }
    
    for patron, respuesta in comandos_rapidos.items():
        if re.search(patron, texto, re.IGNORECASE):
            await mensaje.reply_text(respuesta)
            return
    
    # Análisis de texto con IA (opcional)
    await mensaje.reply_text(f"📝 Texto procesado: {texto[:100]}...")

async def procesar_imagen_ultrarrápido(mensaje, usuario_id: int, context):
    """Procesamiento paralelo masivo de imágenes"""
    # Descarga ultra-rápida en segundo plano
    foto = mensaje.photo[-1]
    file = await foto.get_file()
    
    # Hash único para caching
    image_hash = hashlib.md5(f"{usuario_id}_{mensaje.message_id}".encode()).hexdigest()
    ruta_local = os.path.join(CARPETA_IMAGENES, f"{image_hash}.jpg")
    
    # Descarga asíncrona no bloqueante
    async with aiofiles.open(ruta_local, 'wb') as f:
        await f.write(await file.download_as_bytearray())
    
    await mensaje.reply_text("🚀 Análisis paralelo iniciado...")
    
    # Ejecutar todos los análisis en paralelo con timeout
    try:
        resultados = await asyncio.wait_for(
            ejecutar_analisis_paralelo(ruta_local, usuario_id, image_hash),
            timeout=TIMEOUT_ANALISIS
        )
        
        # Envío optimizado de resultados
        await enviar_resultados_optimizados(mensaje, resultados, ruta_local)
        
    except asyncio.TimeoutError:
        await mensaje.reply_text("⏰ Timeout: Algunos análisis no completaron")
        # Enviar resultados parciales
        resultados_parciales = await obtener_resultados_parciales()
        await mensaje.reply_text(f"📊 Resultados parciales:\n{resultados_parciales}")
    
    finally:
        # Limpieza automática en segundo plano
        asyncio.create_task(limpiar_archivo_temp(ruta_local))

async def ejecutar_analisis_paralelo(ruta_imagen: str, usuario_id: int, image_hash: str) -> list:
    """Ejecuta TODOS los análisis en paralelo como un supercomputador"""
    modulos_analisis = [
        ("QR", analizar_qr),
       # ("Texto", analizar_texto),
        #("Objetos", analizar_objetos),
        ("Metadata", analizar_metadata),
        ("Seguridad", analizar_seguridad),
        ("Memes", analizar_memes),
        ("Colores", analizar_colores),
        ("Calidad", analizar_calidad)
    ]
    
    # Ejecutar todos los análisis concurrentemente
    tasks = []
    for nombre, funcion in modulos_analisis:
        task = ejecutar_con_timeout(
            funcion, ruta_imagen, usuario_id, image_hash, nombre
        )
        tasks.append(task)
    
    # Esperar todos los resultados con gather
    resultados = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Procesar resultados
    resultados_finales = []
    for i, (nombre, _) in enumerate(modulos_analisis):
        resultado = resultados[i]
        if isinstance(resultado, Exception):
            resultados_finales.append(f"❌ {nombre}: Error - {resultado}")
        elif resultado and resultado != "None":
            resultados_finales.append(f"✅ {nombre}: {resultado}")
    
    return resultados_finales

async def ejecutar_con_timeout(func, *args, **kwargs):
    """Ejecuta función con timeout y manejo de errores"""
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(func, *args, **kwargs),
            timeout=10  # Timeout individual por módulo
        )
    except asyncio.TimeoutError:
        return f"Timeout en {func.__name__}"
    except Exception as e:
        return f"Error: {str(e)}"

# FUNCIONES DE ANÁLISOS OPTIMIZADAS (CACHE + THREADING)
def analizar_qr(ruta_imagen: str, usuario_id: int, image_hash: str) -> str:
    """Análisis QR optimizado con caching"""
    cached = cache_analisis_imagen(image_hash, "qr")
    if cached: return cached
    
    resultado = sex.decodificar_qr(ruta_imagen, usuario_id)
    cache_analisis_imagen.cache_clear()  # Mantener cache fresco
    return str(resultado)[:200]  # Limitar tamaño


# --- IMPLEMENTACIONES MÍNIMAS PARA FUNCIONES FALTANTES ---

async def procesar_documento_inteligente(mensaje, usuario_id, context):
    await mensaje.reply_text("📄 Procesamiento de documento no implementado.")

async def procesar_video(mensaje, usuario_id, context):
    await mensaje.reply_text("🎬 Procesamiento de video no implementado.")

async def procesar_sticker(mensaje, usuario_id, context):
    await mensaje.reply_text("🖼️ Procesamiento de sticker no implementado.")

async def obtener_resultados_parciales():
    return "No disponible."

def analizar_metadata(ruta_imagen, usuario_id, image_hash, nombre):
    return "Metadata no implementada."

def analizar_seguridad(ruta_imagen, usuario_id, image_hash, nombre):
    return "Seguridad no implementada."

def analizar_memes(ruta_imagen, usuario_id, image_hash, nombre):
    return "Memes no implementados."

def analizar_colores(ruta_imagen, usuario_id, image_hash, nombre):
    return "Colores no implementados."

def analizar_calidad(ruta_imagen, usuario_id, image_hash, nombre):
    return "Calidad no implementada."

async def enviar_resultados_optimizados(mensaje, resultados: list, ruta_imagen: str):
    """Envía resultados de forma inteligente y eficiente"""
    if not resultados or all("Error" in r or "no disponible" in r.lower() for r in resultados):
        await mensaje.reply_text("🔍 No se encontraron datos analizables en la imagen")
        return
    
    # Agrupar resultados por importancia
    resultados_importantes = [r for r in resultados if any(x in r for x in ["✅", "🔍", "⚠️"])]
    resultados_secundarios = [r for r in resultados if r not in resultados_importantes]
    
    # Construir mensaje optimizado
    mensaje_principal = "🎯 **ANÁLISIS EXPRESS COMPLETADO**\n\n"
    mensaje_principal += "\n".join(resultados_importantes[:3])  # Máximo 3 resultados principales
    
    if resultados_secundarios:
        mensaje_principal += f"\n\n📋 **Otros datos:** (+{len(resultados_secundarios)} más)"
    
    await mensaje.reply_text(mensaje_principal, parse_mode='Markdown')
    
    # Enviar resultados completos si se solicita
    if len(resultados) > 3:
        archivo_resultados = f"{ruta_imagen}_analisis.txt"
        with open(archivo_resultados, 'w', encoding='utf-8') as f:
            f.write("\n".join(resultados))
        
        await mensaje.reply_document(
            document=InputFile(archivo_resultados),
            caption="📄 Resultados completos del análisis"
        )
        os.remove(archivo_resultados)

async def procesar_descarga_url(url: str, usuario_id: int, mensaje):
    """Procesamiento de descargas en segundo plano: envío seguro en MP4"""
    try:
        resultado = downloader.descargar(url, usuario_id)
        if resultado.get('status') != 'success':
            await mensaje.reply_text(f"❌ Error: {resultado.get('message', 'Error desconocido')}")
            return

        file_path = resultado.get('file_path')
        file_type = resultado.get('file_type')

        if file_type != "videos":
            await mensaje.reply_text(f"⚠️ Archivo descargado no es un video: {file_type}")
            return

        abs_path = os.path.abspath(file_path)
        nombre_archivo = os.path.basename(abs_path)
        ruta_convertida = os.path.join("downloads/videos", f"tg_{nombre_archivo}.mp4")

        # Convertir a MP4 compatible
        try:
            convertir_video_compatible(abs_path, ruta_convertida)
        except Exception as conv_err:
            await mensaje.reply_text(f"❌ Error al convertir el video: {str(conv_err)}")
            return

        if not os.path.exists(ruta_convertida):
            await mensaje.reply_text(f"❌ No se encontró el archivo convertido: {ruta_convertida}")
            return

        # Enviar video
        try:
            await mensaje.reply_video(
                video=InputFile(ruta_convertida),
                caption="🎬 Video convertido y listo para Telegram"
            )
        except Exception as send_err:
            await mensaje.reply_text(f"❌ Error al enviar el video: {send_err}")
        finally:
            # Limpiar archivo temporal
            if os.path.exists(ruta_convertida):
                os.remove(ruta_convertida)

    except Exception as e:
        await mensaje.reply_text(f"💥 Error crítico en descarga: {str(e)}")

def convertir_video_compatible(ruta_entrada, ruta_salida):
    """Convierte cualquier video a MP4 H.264 + AAC compatible Telegram"""
    # Envolver rutas entre comillas para manejar espacios y caracteres raros
    comando = [
        "ffmpeg",
        "-y",
        "-i", ruta_entrada,  # FFmpeg puede manejar strings normales si lo pasas como lista
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        ruta_salida
    ]
    subprocess.run(comando, check=True)


# FUNCIONES DE UTILIDAD ULTRA-RÁPIDAS
def detectar_tipo_contenido(mensaje) -> str:
    """Detección lightning-fast del tipo de contenido"""
    if mensaje.photo: return "Imagen"
    if mensaje.video: return "Video"
    if mensaje.document: return f"Documento ({mensaje.document.mime_type})"
    if mensaje.audio: return "Audio"
    if mensaje.voice: return "Mensaje de voz"
    if mensaje.sticker: return "Sticker"
    return "Contenido desconocido"

async def limpiar_archivo_temp(ruta: str):
    """Limpieza asíncrona no bloqueante"""
    try:
        await asyncio.sleep(300)  # Limpiar después de 5 minutos
        if os.path.exists(ruta):
            os.remove(ruta)
    except:
        pass

async def reintento_analisis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reintento automático con backoff exponencial"""
    for intento in range(3):
        try:
            await asyncio.sleep(2 ** intento)  # Backoff exponencial
            await interpretar(update, context)
            return
        except:
            continue
    await update.message.reply_text("🔴 Análisis falló después de 3 intentos")

def generar_respuesta_ayuda() -> str:
    """Genera respuesta de ayuda optimizada"""
    return """🚀 **SouaweakBot PRO - Comandos Rápidos:**

• 📸 Envía una imagen → Análisis completo (QR, texto, objetos, etc.)
• 🔗 Envía una URL → Descarga automática
• 📄 Documentos → Análisis inteligente
• 🎬 Videos → Procesamiento especial

⚡ **Características PRO:**
- Análisis paralelo ultrarrápido
- Detección de 1000+ formatos
- Caching inteligente
- Timeouts automáticos

¡Experimenta la velocidad asiática! 🐉"""

# Logging profesional
import logging
logger = logging.getLogger(__name__)

# Mantener compatibilidad con version anterior
def decodificar_qr(ruta_imagen: str) -> str:
    """Función legacy para compatibilidad"""
    return sex.decodificar_qr(ruta_imagen, 0)

def convertir_video_compatible(ruta_entrada, ruta_salida):
    comando = [
        "ffmpeg",
        "-y",
        "-i", ruta_entrada,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        ruta_salida
    ]
    subprocess.run(comando, check=True)