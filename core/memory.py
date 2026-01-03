import psutil

def get_memory():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "ram": {
            "total_gb": round(mem.total / 1024**3, 2),
            "used_gb": round(mem.used / 1024**3, 2),
            "available_gb": round(mem.available / 1024**3, 2),
            "percent": mem.percent
        },
        "swap": {
            "total_gb": round(swap.total / 1024**3, 2),
            "used_gb": round(swap.used / 1024**3, 2),
            "percent": swap.percent
        }
    }
