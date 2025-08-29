# modulos/resource_manager.py
import psutil
import shutil
import logging

logger = logging.getLogger(__name__)

def verificar_recursos(min_cpu=20, min_ram_mb=200, min_disk_mb=500):
    """
    Retorna True si hay suficientes recursos:
    - CPU libre en porcentaje
    - RAM libre en MB
    - Espacio libre en disco en MB
    """
    cpu_libre = 100 - psutil.cpu_percent(interval=0.5)
    ram_libre = psutil.virtual_memory().available / 1024 / 1024
    disco_libre = shutil.disk_usage(".").free / 1024 / 1024

    if cpu_libre < min_cpu:
        logger.warning(f"[resource_manager] CPU baja: {cpu_libre:.2f}% libre")
        return False
    if ram_libre < min_ram_mb:
        logger.warning(f"[resource_manager] RAM baja: {ram_libre:.2f} MB libre")
        return False
    if disco_libre < min_disk_mb:
        logger.warning(f"[resource_manager] Disco bajo: {disco_libre:.2f} MB libre")
        return False

    return True

def priorizar_tarea(tarea_name="tarea"):
    """
    Aquí podrías implementar lógica de prioridad según recursos actuales
    """
    cpu_libre = 100 - psutil.cpu_percent(interval=0.5)
    if cpu_libre < 50:
        logger.info(f"[resource_manager] Recursos bajos, retrasando {tarea_name}")
        return False
    return True