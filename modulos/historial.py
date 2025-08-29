"""
historial.py
Mantiene un registro completo de descargas por usuario.
Compatible con videos, fotos, mangas, QR y más.
"""

import os
import json
from datetime import datetime

HISTORIAL_PATH = "downloads/historial/"  # Carpeta donde se guardan archivos JSON

# Crear carpeta si no existe
os.makedirs(HISTORIAL_PATH, exist_ok=True)

def _ruta_usuario(usuario_id: int):
    """Ruta del archivo JSON de un usuario"""
    return os.path.join(HISTORIAL_PATH, f"{usuario_id}.json")

def registrar(usuario_id: int, nombre_archivo: str, tipo: str, url: str = "", duracion: str = ""):
    """
    Registra una descarga en el historial del usuario.
    """
    registro = {
        "nombre": nombre_archivo,
        "tipo": tipo,
        "url": url,
        "duracion": duracion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    ruta = _ruta_usuario(usuario_id)
    historial = []

    # Cargar historial existente
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            try:
                historial = json.load(f)
            except:
                historial = []

    # Añadir nuevo registro
    historial.append(registro)

    # Guardar nuevamente
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

def obtener(usuario_id: int, tipo: str = None):
    """
    Obtiene historial completo del usuario.
    Si tipo se especifica, filtra por tipo de archivo (videos, fotos, mangas, etc.)
    """
    ruta = _ruta_usuario(usuario_id)
    if not os.path.exists(ruta):
        return []

    with open(ruta, "r", encoding="utf-8") as f:
        historial = json.load(f)

    if tipo:
        historial = [h for h in historial if h["tipo"] == tipo]

    return historial

def limpiar(usuario_id: int):
    """
    Limpia todo el historial de un usuario.
    """
    ruta = _ruta_usuario(usuario_id)
    if os.path.exists(ruta):
        os.remove(ruta)
        return True
    return False

def ultimo(usuario_id: int, n: int = 5):
    """
    Obtiene los últimos n registros del usuario.
    """
    historial_usuario = obtener(usuario_id)
    return historial_usuario[-n:] if historial_usuario else []

def mostrar(usuario_id: int, tipo: str = None):
    """
    Retorna un texto listo para enviar al chat con el historial del usuario.
    """
    registros = obtener(usuario_id, tipo)
    if not registros:
        return "No tienes historial registrado."

    texto = f"📜 Historial de descargas (Usuario {usuario_id}):\n\n"
    for i, r in enumerate(registros, 1):
        texto += f"{i}. {r['tipo'].capitalize()}: {r['nombre']}\n   URL: {r['url']}\n   Fecha: {r['fecha']}\n"
        if r.get("duracion"):
            texto += f"   Duración: {r['duracion']}\n"
    return texto