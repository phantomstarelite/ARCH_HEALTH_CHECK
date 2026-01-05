

# 🩺 ArchHealth – Arch Linux System Health Monitor

**ArchHealth** is a modern, lightweight **system health monitoring tool for Arch Linux**, providing real-time insights into CPU, memory, SSD, battery, GPU, and overall system health through both **CLI/TUI** and **modern PyQt GUI**.

Designed with **clean architecture**, **industry-standard UI**, and **extensibility** in mind.

---

## ✨ Features

### ✅ Core Monitoring

* **CPU**

  * Usage percentage
  * Frequency
  * Temperature
* **Memory**

  * RAM usage (used / total)
  * Swap usage
* **SSD / NVMe**

  * SMART health status
  * Wear percentage
* **Battery**

  * Charge percentage
  * Wear estimation (if available)
* **GPU**

  * Intel iGPU / NVIDIA Optimus detection
* **System Services**

  * Failed systemd services count

---

### 📊 Health Score Engine

* Computes an **overall health score (0–100)**
* Intelligent deductions based on:

  * High temperatures
  * High resource usage
  * SSD wear
  * Battery degradation
  * Failed services

---

### 🖥️ User Interfaces

#### 🔹 CLI / TUI (Terminal)

* Rich-based dashboard
* Live monitoring (`--watch`)
* Lightweight and fast

#### 🔹 Modern GUI (PyQt6)

* Dark, modern UI
* Card-based layout
* Progress bars with percentages
* Auto-refresh
* User-friendly and readable

---

## 📸 Screenshots

> *(Add screenshots here)*
> Example:

```text
screenshots/
 ├── gui.png
 ├── tui.png
```

---

## 🏗️ Project Architecture

```
arch-health-check/
├── core/          # System data collectors
│   ├── cpu.py
│   ├── memory.py
│   ├── ssd.py
│   ├── battery.py
│   ├── gpu.py
│   ├── temps.py
│   └── system.py
├── engine/        # Health scoring logic
│   └── score_v2.py
├── ui/            # User interfaces
│   ├── dashboard.py   # TUI (Rich)
│   └── gui.py         # PyQt GUI
├── cli.py         # CLI entry point
├── main.py        # App coordinator
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/yourusername/archhealth.git
cd archhealth
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

> On Arch Linux, make sure Qt is installed:

```bash
sudo pacman -S qt6-base qt6-wayland
```

---

## ▶️ Usage

### 🔹 Run CLI / TUI

```bash
python cli.py
```

Live monitoring:

```bash
python cli.py --watch
```

---

### 🔹 Run GUI

```bash
python - <<EOF
from ui.gui import launch_gui
launch_gui()
EOF
```

---

## 🔐 Permissions

Some features (SSD SMART, temperatures) require elevated permissions.

Currently:

* `smartctl` runs via `sudo`

> 🔧 Planned improvement: **polkit integration** (no sudo prompts)

---

## 🧠 Design Philosophy

* **Modular architecture** (easy to extend)
* **Clear data contracts** between collectors, engine, and UI
* **Defensive coding** (safe `.get()` access)
* **Linux-native tooling**
* **No unnecessary background services**

---

## 🚀 Roadmap

Planned enhancements:

* [ ] System tray widget
* [ ] Historical charts (CPU/RAM trends)
* [ ] Temperature-specific bars
* [ ] AppImage / Flatpak packaging
* [ ] Polkit support (remove sudo)
* [ ] Arch PKGBUILD

---

## 🤝 Contributing

Contributions are welcome!

* Fork the repo
* Create a feature branch
* Follow existing architecture
* Submit a PR

---

## 📜 License

MIT License
Feel free to use, modify, and distribute.

---

## 👤 Author

**Pratik**
Arch Linux | Python | System Tools
Built as a learning + showcase project with real-world architecture.

---

## ⭐ Acknowledgements

* Arch Linux community
* psutil
* lm_sensors
* smartmontools
* PyQt6
* Rich

---

### ⭐ If you like this project, give it a star!

