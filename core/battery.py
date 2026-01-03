import psutil
import os

POWER_SUPPLY_PATH = "/sys/class/power_supply"

def read_sys_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return None


def get_battery_health():
    battery = psutil.sensors_battery()
    if not battery:
        return {"present": False}

    bat_dir = None
    for item in os.listdir(POWER_SUPPLY_PATH):
        if item.startswith("BAT"):
            bat_dir = os.path.join(POWER_SUPPLY_PATH, item)
            break

    if not bat_dir:
        return {"present": False}

    energy_full = read_sys_file(f"{bat_dir}/energy_full")
    energy_full_design = read_sys_file(f"{bat_dir}/energy_full_design")
    cycle_count = read_sys_file(f"{bat_dir}/cycle_count")

    health = None
    wear = None

    if energy_full and energy_full_design:
        energy_full = int(energy_full)
        energy_full_design = int(energy_full_design)
        health = round((energy_full / energy_full_design) * 100, 2)
        wear = round(100 - health, 2)

    return {
        "present": True,
        "percent": battery.percent,
        "plugged": battery.power_plugged,
        "time_left_min": battery.secsleft // 60 if battery.secsleft > 0 else None,
        "health_percent": health,
        "wear_percent": wear,
        "cycle_count": int(cycle_count) if cycle_count else None
    }
