"""
resource_manager.py
Monitoreo y gestión de recursos de la laptop para SouaweakBot.
Controla CPU, RAM, espacio en disco y prioriza tareas.
"""

import psutil
import shutil
from modulos import historial

# Configuración de límites (puedes ajustarlos)
LIMITE_RAM = 0.85  # 85% de uso máximo permitido
LIMITE_CPU = 90    # 90% de uso máximo permitido
LIMITE_DISCO_GB = 2  # mínimo de GB libres en disco

def verificar_recursos() -> bool:
    """
    Verifica si hay recursos suficientes para ejecutar tareas pesadas.
    Retorna True si todo está dentro del límite, False si hay saturación.
    """
    ram = psutil.virtual_memory().percent / 100
    cpu = psutil.cpu_percent(interval=1)
    disco_libre_gb = shutil.disk_usage(".").free / (1024 ** 3)

    if ram > LIMITE_RAM:
        print(f"[resource_manager] RAM alta: {ram*100:.1f}%")
        return False
    if cpu > LIMITE_CPU:
        print(f"[resource_manager] CPU alta: {cpu:.1f}%")
        return False
    if disco_libre_gb < LIMITE_DISCO_GB:
        print(f"[resource_manager] Espacio en disco bajo: {disco_libre_gb:.2f}GB")
        return False

    return True

def pausar_modulo(modulo_nombre: str):
    """
    Placeholder para pausar un módulo activo.
    """
    print(f"[resource_manager] Pausando módulo: {modulo_nombre}")

def reanudar_modulo(modulo_nombre: str):
    """
    Placeholder para reanudar un módulo pausado.
    """
    print(f"[resource_manager] Reanudando módulo: {modulo_nombre}")

def priorizar_tarea(tarea_nombre: str):
    """
    Placeholder para priorizar una tarea crítica.
    """
    print(f"[resource_manager] Priorizando tarea: {tarea_nombre}")