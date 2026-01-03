import subprocess
import re

NVME_DEVICE = "/dev/nvme0n1"


def run_smartctl():
    """
    Runs smartctl for the NVMe device and returns raw output.
    """
    try:
        return subprocess.check_output(
            ["sudo", "smartctl", "-a", NVME_DEVICE],
            text=True
        )
    except Exception:
        return None


def parse_nvme_smart(output: str):
    data = {
        "health": "UNKNOWN",
        "wear_percent": None,
        "available_spare": None,
        "spare_threshold": None,
        "data_written_tb": None,
        "data_read_tb": None,
        "power_on_hours": None,
        "power_cycles": None,
        "unsafe_shutdowns": None,
        "media_errors": None,
        "critical_warning": None,
        "temperature_c": None
    }

    if not output:
        data["health"] = "ERROR"
        return data

    if "PASSED" in output:
        data["health"] = "PASSED"
    elif "FAILED" in output:
        data["health"] = "FAILED"

    patterns = {
        "wear_percent": r"Percentage Used:\s+(\d+)%",
        "available_spare": r"Available Spare:\s+(\d+)%",
        "spare_threshold": r"Available Spare Threshold:\s+(\d+)%",
        "power_on_hours": r"Power On Hours:\s+([\d,]+)",
        "power_cycles": r"Power Cycles:\s+([\d,]+)",
        "unsafe_shutdowns": r"Unsafe Shutdowns:\s+([\d,]+)",
        "media_errors": r"Media and Data Integrity Errors:\s+(\d+)",
        "critical_warning": r"Critical Warning:\s+0x([0-9a-fA-F]+)",
        "temperature_c": r"Temperature:\s+(\d+)\s+Celsius"
    }

    for key, pattern in patterns.items():
        m = re.search(pattern, output)
        if m:
            data[key] = int(m.group(1).replace(",", ""))

    # Data written
    m = re.search(r"Data Units Written:\s+([\d,]+)", output)
    if m:
        units = int(m.group(1).replace(",", ""))
        data["data_written_tb"] = round((units * 512_000) / (1024 ** 4), 2)

    # Data read
    m = re.search(r"Data Units Read:\s+([\d,]+)", output)
    if m:
        units = int(m.group(1).replace(",", ""))
        data["data_read_tb"] = round((units * 512_000) / (1024 ** 4), 2)

    return data


def get_ssd_health():
    """
    Public API used by main.py
    """
    raw = run_smartctl()
    return parse_nvme_smart(raw)
