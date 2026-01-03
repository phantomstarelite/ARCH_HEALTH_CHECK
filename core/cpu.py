import psutil
import platform


def get_cpu():
    """
    Collect detailed CPU information for health monitoring.
    """

    freq = psutil.cpu_freq()
    load1, load5, load15 = psutil.getloadavg()

    return {
        "model": platform.processor(),
        "cores_logical": psutil.cpu_count(logical=True),
        "cores_physical": psutil.cpu_count(logical=False),
        "usage_percent": psutil.cpu_percent(interval=1),
        "frequency_mhz": round(freq.current, 2) if freq else None,
        "frequency_max_mhz": round(freq.max, 2) if freq else None,
        "load_avg": {
            "1min": round(load1, 2),
            "5min": round(load5, 2),
            "15min": round(load15, 2),
        }
    }
