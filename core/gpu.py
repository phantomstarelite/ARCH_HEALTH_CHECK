import subprocess
import shutil
import os

def run(cmd):
    try:
        return subprocess.check_output(cmd, text=True).strip()
    except Exception:
        return None


# -----------------------------
# NVIDIA GPU
# -----------------------------
def get_nvidia_gpu():
    if not shutil.which("nvidia-smi"):
        return None

    out = run([
        "nvidia-smi",
        "--query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.state",
        "--format=csv,noheader,nounits"
    ])

    if not out:
        return None

    name, temp, util, mem_used, mem_total, pstate = out.split(", ")

    return {
        "vendor": "NVIDIA",
        "card": "card0",
        "name": name,
        "temperature": int(temp),
        "utilization": int(util),
        "vram_used_mb": int(mem_used),
        "vram_total_mb": int(mem_total),
        "power_state": pstate
    }


# -----------------------------
# Intel GPU (card1 confirmed)
# -----------------------------
def get_intel_gpu():
    base = "/sys/class/drm/card1"

    try:
        with open(f"{base}/device/vendor") as f:
            if f.read().strip() != "0x8086":
                return None
    except Exception:
        return None

    freq = run(["cat", f"{base}/gt_cur_freq_mhz"])
    max_freq = run(["cat", f"{base}/gt_max_freq_mhz"])

    return {
        "vendor": "Intel",
        "card": "card1",
        "frequency_mhz": int(freq) if freq else None,
        "max_frequency_mhz": int(max_freq) if max_freq else None
    }


def get_gpu_health():
    return {
        "intel": get_intel_gpu(),
        "nvidia": get_nvidia_gpu()
    }
