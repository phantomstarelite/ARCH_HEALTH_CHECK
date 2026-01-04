import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QProgressBar, QFrame
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

from core.cpu import get_cpu
from core.memory import get_memory
from core.ssd import get_ssd_health
from core.battery import get_battery_health
from core.gpu import get_gpu_health
from core.system import failed_services
from core.temps import get_temperatures
from engine.score_v2 import calculate_health


# =========================
# Metric Card (Reusable)
# =========================
class MetricCard(QFrame):
    def __init__(self, title: str):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border-radius: 12px;
                padding: 14px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        self.title = QLabel(title)
        self.title.setStyleSheet("color: #cdd6f4; font-size: 13px;")

        self.value = QLabel("--")
        self.value.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(10)

        self.bar.setStyleSheet("""
            QProgressBar {
                background-color: #313244;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 5px;
            }
        """)

        self.subtext = QLabel("")
        self.subtext.setStyleSheet("color: #a6adc8; font-size: 11px;")

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addWidget(self.bar)
        layout.addWidget(self.subtext)

    def update(self, percent: int, subtext: str = "", color: str = "#89b4fa"):
        self.value.setText(f"{percent} %")
        self.bar.setValue(percent)

        self.bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #313244;
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
        """)

        self.subtext.setText(subtext)


# =========================
# Main Window
# =========================
class HealthWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Arch Health Monitor")
        self.setMinimumSize(420, 600)
        self.setStyleSheet("background-color: #11111b; color: #cdd6f4;")

        main = QVBoxLayout(self)
        main.setSpacing(16)

        # Title
        title = QLabel("🩺 Arch System Health")
        title.setFont(QFont("Inter", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(title)

        # Score
        self.score_label = QLabel("-- / 100")
        self.score_label.setFont(QFont("Inter", 28, QFont.Weight.Bold))
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main.addWidget(self.score_label)

        # Metric Cards
        self.cpu_card = MetricCard("CPU Usage")
        self.mem_card = MetricCard("Memory Usage")
        self.ssd_card = MetricCard("SSD Wear")
        self.bat_card = MetricCard("Battery")
        self.gpu_card = MetricCard("GPU")

        # GPU is text-only
        self.gpu_card.bar.hide()

        main.addWidget(self.cpu_card)
        main.addWidget(self.mem_card)
        main.addWidget(self.ssd_card)
        main.addWidget(self.bat_card)
        main.addWidget(self.gpu_card)

        # Auto refresh every 3 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(3000)

        self.refresh()

    def refresh(self):
        data = {
            "cpu": get_cpu(),
            "memory": get_memory(),
            "temps": get_temperatures(),
            "ssd": get_ssd_health(),
            "battery": get_battery_health(),
            "gpu": get_gpu_health(),
            "services": failed_services(),
        }

        score, _ = calculate_health(data)
        self.score_label.setText(f"{score} / 100")

        if score >= 80:
            self.score_label.setStyleSheet("color: #a6e3a1;")
        elif score >= 60:
            self.score_label.setStyleSheet("color: #f9e2af;")
        else:
            self.score_label.setStyleSheet("color: #f38ba8;")

        # CPU
        cpu = data["cpu"]
        cpu_usage = int(cpu["usage_percent"])
        cpu_temp = data["temps"]["cpu"]["current"]
        self.cpu_card.update(
            cpu_usage,
            f"Temp: {cpu_temp}°C | Freq: {cpu['frequency_mhz']} MHz",
            "#a6e3a1" if cpu_usage < 70 else "#f9e2af" if cpu_usage < 90 else "#f38ba8"
        )

        # Memory
        ram = data["memory"]["ram"]
        self.mem_card.update(
            int(ram["percent"]),
            f"{ram['used_gb']} / {ram['total_gb']} GB"
        )

        # SSD
        wear = data["ssd"]["wear_percent"] or 0
        self.ssd_card.update(
            wear,
            f"Health: {data['ssd']['health']}",
            "#a6e3a1" if wear < 30 else "#f9e2af" if wear < 60 else "#f38ba8"
        )

        # Battery
        battery = data["battery"]

        if battery:
            bat = int(battery["percent"])

            charging = battery.get("charging")
            if charging is True:
                status = "Charging"
            elif charging is False:
                status = "On Battery"
            else:
                status = "Battery Status Unknown"

            self.bat_card.update(
                bat,
                status,
                "#a6e3a1" if bat > 50 else "#f9e2af" if bat > 20 else "#f38ba8"
            )
        else:
            self.bat_card.update(0, "No Battery")
        

        # GPU
        self.gpu_card.value.setText(
            "NVIDIA Active" if data["gpu"]["nvidia"] else "Intel / Optimus"
        )
        self.gpu_card.subtext.setText("")


# =========================
# Launch GUI
# =========================
def launch_gui():
    app = QApplication(sys.argv)
    win = HealthWindow()
    win.show()
    sys.exit(app.exec())
