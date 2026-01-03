from core.cpu import get_cpu
from core.memory import get_memory
from core.temps import get_temperatures
from core.ssd import get_ssd_health
from core.battery import get_battery_health
from core.gpu import get_gpu_health
from core.system import failed_services

from engine.score_v2 import calculate_health
from ui.dashboard import render_dashboard


def main():
    data = {
        "cpu": get_cpu(),
        "memory": get_memory(),
        "temps": get_temperatures(),
        "ssd": get_ssd_health(),
        "battery": get_battery_health(),
        "gpu": get_gpu_health(),
        "services": failed_services(),
    }

    score, issues = calculate_health(data)
    render_dashboard(data, score, issues)


if __name__ == "__main__":
    main()
