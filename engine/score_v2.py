def clamp(val, min_v=0, max_v=100):
    return max(min_v, min(val, max_v))


def score_cpu(cpu, temps):
    score = 25
    issues = []

    if not cpu or not temps or "cpu" not in temps:
        return score, issues

    temp = temps["cpu"]["current"]

    if temp >= 90:
        score -= 15
        issues.append(f"CPU overheating ({temp}°C)")
    elif temp >= 80:
        score -= 8
        issues.append(f"CPU temperature high ({temp}°C)")

    usage = cpu.get("usage_percent")
    if usage is not None and usage > 90:
        score -= 5
        issues.append("High CPU usage")

    return clamp(score, 0, 25), issues


def score_ssd(ssd, temps):
    score = 25
    issues = []

    if not ssd:
        return score, issues

    if ssd["health"] != "PASSED":
        score -= 15
        issues.append("SSD SMART health check failed")

    wear = ssd.get("wear_percent")
    if wear is not None:
        if wear >= 80:
            score -= 10
            issues.append("SSD near end of life")
        elif wear >= 50:
            score -= 5
            issues.append("SSD wear increasing")

    if temps and "nvme" in temps:
        nvme_temp = temps["nvme"]["current"]
        if nvme_temp >= 80:
            score -= 10
            issues.append(f"SSD overheating ({nvme_temp}°C)")
        elif nvme_temp >= 70:
            score -= 5
            issues.append(f"SSD temperature high ({nvme_temp}°C)")

    return clamp(score, 0, 25), issues


def score_memory(mem):
    score = 15
    issues = []

    if not mem:
        return score, issues

    ram = mem.get("ram", {})
    swap = mem.get("swap", {})

    ram_percent = ram.get("percent")
    swap_percent = swap.get("percent")

    if ram_percent is not None:
        if ram_percent >= 95:
            score -= 10
            issues.append("RAM critically high usage")
        elif ram_percent >= 85:
            score -= 5
            issues.append("RAM usage high")

    if swap_percent is not None and swap_percent >= 80:
        score -= 5
        issues.append("Swap heavily used")

    return clamp(score, 0, 15), issues


def score_battery(bat):
    score = 15
    issues = []

    if not bat or not bat.get("present"):
        return score, issues

    wear = bat.get("wear_percent")
    if wear is not None:
        if wear >= 40:
            score -= 10
            issues.append("Battery heavily worn")
        elif wear >= 25:
            score -= 5
            issues.append("Battery wear noticeable")

    return clamp(score, 0, 15), issues


def score_gpu(gpu):
    score = 10
    issues = []

    if not gpu:
        return score, issues

    nvidia = gpu.get("nvidia")
    if not nvidia:
        return score, issues  # Optimus inactive is OK

    temp = nvidia["temperature"]
    if temp >= 85:
        score -= 7
        issues.append("NVIDIA GPU overheating")
    elif temp >= 75:
        score -= 3
        issues.append("NVIDIA GPU temperature high")

    return clamp(score, 0, 10), issues


def score_services(failed):
    score = 10
    issues = []

    if failed > 0:
        score -= min(10, failed * 2)
        issues.append(f"{failed} failed system services")

    return clamp(score, 0, 10), issues


def calculate_health(data):
    total = 0
    issues = []

    for s, i in [
        score_cpu(data.get("cpu"), data.get("temps")),
        score_ssd(data.get("ssd"), data.get("temps")),
        score_memory(data.get("memory")),
        score_battery(data.get("battery")),
        score_gpu(data.get("gpu")),
        score_services(data.get("services", 0)),
    ]:
        total += s
        issues.extend(i)

    return clamp(total), issues
