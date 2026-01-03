import subprocess

def failed_services():
    try:
        out = subprocess.check_output(
            ["systemctl", "--failed", "--no-legend"],
            text=True
        )
        return len(out.strip().splitlines()) if out.strip() else 0
    except Exception:
        return 0
