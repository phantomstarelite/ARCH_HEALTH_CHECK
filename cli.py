import argparse
import time
import os
from main import main

def run():
    parser = argparse.ArgumentParser(
        description="Arch System Health Monitor"
    )

    parser.add_argument(
        "--watch",
        action="store_true",
        help="Live refresh mode"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=3,
        help="Refresh interval in seconds"
    )

    args = parser.parse_args()

    if args.watch:
        try:
            while True:
                os.system("clear")
                main()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nExiting watch mode 👋")
    else:
        main()

# 🔴 THIS WAS MISSING — ABSOLUTELY REQUIRED
if __name__ == "__main__":
    run()
