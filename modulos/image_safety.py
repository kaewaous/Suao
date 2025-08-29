"""
image_safety.py
Filtra imágenes NSFW o sensibles usando un modelo pre-entrenado.
"""

from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch
from modulos import historial

# Modelo NSFW ejemplo
modelo_id = "openai/clip-vit-base-patch32"  # puedes reemplazar por un modelo NSFW real
extractor = AutoFeatureExtractor.from_pretrained(modelo_id)
modelo = AutoModelForImageClassification.from_pretrained(modelo_id)

def analizar_safety(ruta_imagen: str, usuario_id: int):
    imagen = Image.open(ruta_imagen).convert("RGB")
    inputs = extractor(images=imagen, return_tensors="pt")
    with torch.no_grad():
        outputs = modelo(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        # Para un modelo NSFW real habría clases NSFW y SFW
        clase_idx = probs.argmax().item()
        clase_nombre = modelo.config.id2label[clase_idx]

    # Guardar en historial
    historial.registrar(usuario_id, ruta_imagen, tipo="safety", url="")

    return f"[image_safety] Clasificación: {clase_nombre} ({probs[0, clase_idx]:.2f})"