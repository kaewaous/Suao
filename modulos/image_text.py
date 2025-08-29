"""
image_text.py
Convierte texto en imágenes a texto editable usando OCR.
"""

import pytesseract
from PIL import Image
from modulos import historial

def extraer_texto(ruta_imagen: str, usuario_id: int):
    imagen = Image.open(ruta_imagen)
    texto = pytesseract.image_to_string(imagen, lang='eng')  # puedes agregar 'spa' si quieres español

    if not texto.strip():
        resultado = "[image_text] No se detectó texto en la imagen."
    else:
        resultado = f"[image_text] Texto detectado: {texto}"

    # Guardar en historial
    historial.registrar(usuario_id, ruta_imagen, tipo="ocr", url="")

    return resultado