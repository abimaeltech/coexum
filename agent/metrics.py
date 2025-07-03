"""
Coleta métricas locais de CPU, memória e uptime.
"""
import psutil

def collect_metrics() -> dict:
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'boot_time': psutil.boot_time(),
    }
