"""
image_objects.py
Detección de objetos y escenas reales usando YOLOv8.
"""

from ultralytics import YOLO
import cv2
from modulos import historial

# Cargar modelo pre-entrenado YOLOv8s
modelo = YOLO("yolov8s.pt")  # Peso oficial ligero

def detectar_objetos(ruta_imagen: str, usuario_id: int):
    """
    Detecta objetos y escenas en la imagen.
    Devuelve lista de objetos detectados con su confianza.
    """
    imagen = cv2.imread(ruta_imagen)
    resultados = modelo.predict(imagen, imgsz=640, conf=0.25, verbose=False)[0]  # conf=umbral

    objetos_detectados = []
    for caja in resultados.boxes:
        clase = modelo.names[int(caja.cls)]
        conf = float(caja.conf)
        objetos_detectados.append(f"{clase} ({conf:.2f})")

    # Guardar en historial
    historial.registrar(usuario_id, ruta_imagen, tipo="objetos", url="")

    if not objetos_detectados:
        return "[image_objects] No se detectaron objetos."
    return f"[image_objects] Objetos detectados: {', '.join(objetos_detectados)}"