"""
image_metadata.py
Extrae metadatos EXIF y GPS de imágenes.
"""

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from modulos import historial

def extraer_metadata(ruta_imagen: str, usuario_id: int):
    imagen = Image.open(ruta_imagen)
    exif_data = imagen._getexif()
    if not exif_data:
        return "[image_metadata] No se encontraron metadatos EXIF."

    metadata = {}
    gps_info = {}
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == "GPSInfo":
            for key in value:
                gps_tag = GPSTAGS.get(key, key)
                gps_info[gps_tag] = value[key]
        else:
            metadata[tag] = value

    resultado = f"[image_metadata] Metadatos: {metadata}, GPS: {gps_info}"

    # Guardar en historial
    historial.registrar(usuario_id, ruta_imagen, tipo="metadata", url="")

    return resultado