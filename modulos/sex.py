"""
sex.py
Decodificación completa de códigos QR: WiFi, URLs, texto, correos, etc.
Funciona 100% real con pyzbar y validators.
"""

import re
import cv2
from pyzbar import pyzbar
from modulos import historial
import validators

def decodificar_qr(ruta_imagen: str, usuario_id: int):
    """
    Decodifica todos los códigos QR en la imagen y determina tipo: WiFi, URL, Email, texto plano.
    Registra automáticamente en historial.
    """
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        return "[sex] Error: no se pudo cargar la imagen."

    codigos = pyzbar.decode(imagen)
    resultados = []

    for codigo in codigos:
        datos = codigo.data.decode('utf-8')
        tipo_qr = codigo.type
        info_extra = ""

        # Intentar detectar QR tipo WiFi (formato estándar: WIFI:T:WPA;S:SSID;P:PASS;;)
        wifi_match = re.match(r'WIFI:T:(.*?);S:(.*?);P:(.*?);;', datos)
        if wifi_match:
            tipo, ssid, password = wifi_match.groups()
            info_extra = f"SSID: {ssid}, Tipo: {tipo}, Contraseña: {password}"
            resultado = f"[sex] QR WiFi detectado: {info_extra}"

        # Detectar URL
        elif validators.url(datos):
            resultado = f"[sex] QR URL detectado: {datos}"

        # Detectar correo
        elif validators.email(datos):
            resultado = f"[sex] QR Email detectado: {datos}"

        # Texto plano
        else:
            resultado = f"[sex] QR texto detectado: {datos}"

        resultados.append(resultado)

        # Registrar en historial
        historial.registrar(usuario_id, f"QR_{tipo_qr}", tipo="qr", url=datos)

    if not resultados:
        return "[sex] No se detectó ningún QR."

    return resultados