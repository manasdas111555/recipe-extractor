"""
Universal Pro AI — Celery Worker Runner Script
==============================================
Starts the distributed extraction worker with automatic platform detection.
On Windows: Uses `--pool=solo` to prevent Win32 multiprocessing fork errors.
On Linux/macOS: Uses standard pre-fork concurrency.
"""

import sys
import os
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

def main():
    print("=" * 60)
    print("🚀 Starting Universal Pro AI Distributed Celery Worker...")
    print(f"📁 Project Root: {ROOT_DIR}")
    print(f"💻 OS Platform: {sys.platform}")
    print("=" * 60)

    # Windows does not support POSIX fork(); force --pool=solo
    pool_arg = "--pool=solo" if sys.platform == "win32" else "--concurrency=4"
    log_level = os.getenv("CELERY_LOG_LEVEL", "INFO")

    cmd = [
        sys.executable,
        "-m",
        "celery",
        "-A",
        "backend.app.workers.celery_app:celery_app",
        "worker",
        pool_arg,
        f"--loglevel={log_level}"
    ]

    print(f"👉 Executing: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, cwd=str(ROOT_DIR))
    except KeyboardInterrupt:
        print("\n🛑 Celery worker stopped by user.")

if __name__ == "__main__":
    main()
