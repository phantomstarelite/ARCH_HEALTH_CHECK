from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def render_dashboard(data, score, issues):
    table = Table(title="🩺 Arch System Health Monitor", show_lines=True)

    table.add_column("Component", style="bold")
    table.add_column("Details")

    # ── CPU ─────────────────────────────
    cpu = data["cpu"]
    table.add_row(
        "CPU",
        f"Usage: {cpu.get('usage_percent', 'N/A')}% | "
        f"Cores: {cpu.get('cores_physical', 'N/A')}P/"
        f"{cpu.get('cores_logical', 'N/A')}L | "
        f"Freq: {cpu.get('frequency_mhz', 'N/A')} MHz"
)


    # ── Memory ──────────────────────────
    mem = data["memory"]
    table.add_row(
        "Memory",
        f'RAM {mem["ram"]["percent"]}% '
        f'({mem["ram"]["used_gb"]}/{mem["ram"]["total_gb"]} GB) | '
        f'Swap {mem["swap"]["percent"]}%'
)


    # ── SSD ─────────────────────────────
    ssd = data["ssd"]
    ssd_details = [
        f"Health: {ssd['health']}",
        f"Wear: {ssd['wear_percent']}%"
    ]

    # Optional extended SSD info (if present)
    if "data_written_tb" in ssd and ssd["data_written_tb"] is not None:
        ssd_details.append(f"TBW: {ssd['data_written_tb']} TB")
    if "power_on_hours" in ssd and ssd["power_on_hours"] is not None:
        ssd_details.append(f"POH: {ssd['power_on_hours']} h")
    if "unsafe_shutdowns" in ssd and ssd["unsafe_shutdowns"] is not None:
        ssd_details.append(f"Unsafe: {ssd['unsafe_shutdowns']}")

    table.add_row("SSD", " | ".join(ssd_details))

    # ── Battery ─────────────────────────
    bat = data["battery"]
    if bat and bat.get("present"):
        table.add_row(
            "Battery",
            f"{bat['percent']}% | Wear {bat['wear_percent']}% | Cycles {bat.get('cycle_count', 'N/A')}"
        )
    else:
        table.add_row("Battery", "Not detected")

    # ── GPU ─────────────────────────────
    gpu = data["gpu"]
    if gpu["nvidia"]:
        ng = gpu["nvidia"]
        table.add_row(
            "NVIDIA GPU",
            f"{ng['temperature']}°C | VRAM {ng['vram_used_mb']}/{ng['vram_total_mb']} MB | {ng['power_state']}"
        )
    else:
        table.add_row("GPU", "Intel iGPU (Optimus, power-saving)")

    # ── Services ────────────────────────
    table.add_row("Failed Services", str(data["services"]))

    # ── Render ──────────────────────────
    console.print(table)
    console.print(
        Panel(
            f"{score}/100",
            title="Overall Health Score",
            style="green" if score >= 80 else "yellow"
        )
    )

    if issues:
        console.print(
            Panel("\n".join(issues), title="⚠ Issues Detected", style="red")
        )
    else:
        console.print(
            Panel("System is healthy ✔", style="green")
        )
