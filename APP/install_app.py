#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
import time

VENV_DIR = ".venv"

# --------------------------------------------------
# Helpers
# --------------------------------------------------
def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def run(cmd):
    log(f"▶ {cmd}")
    result = subprocess.call(cmd, shell=True)
    if result != 0:
        print(f"\n❌ FAILED: {cmd}")
        sys.exit(1)

def venv_python():
    if platform.system() == "Windows":
        return os.path.join(VENV_DIR, "Scripts", "python")
    return os.path.join(VENV_DIR, "bin", "python")

# --------------------------------------------------
# Main
# --------------------------------------------------
def main():
    print("=" * 70)
    print("🚀 EthoGrid-ToxMate Installer (PURE PYTHON / FAST)")
    print("=" * 70)

    log(f"OS Detected: {platform.system()}")

    # --------------------------------------------------
    # 1. Create virtual environment
    # --------------------------------------------------
    log("STEP 1/5: Checking virtual environment...")
    if os.path.exists(VENV_DIR):
        log("Virtual environment already exists → skipping creation")
    else:
        log("Creating virtual environment...")
        run(f"{sys.executable} -m venv {VENV_DIR}")

    py = venv_python()

    # --------------------------------------------------
    # 2. Upgrade pip + build tools
    # --------------------------------------------------
    log("STEP 2/5: Upgrading pip & wheel...")
    run(f"{py} -m pip install --upgrade pip wheel setuptools")

    # --------------------------------------------------
    # 3. Install ALL core dependencies (one call)
    # --------------------------------------------------
    log("STEP 3/5: Installing core packages...")

    core_packages = [
        "numpy==1.26.*",
        "opencv-python",
        "PyQt5",
        "scipy",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "torch",
        "torchvision",
        "torchaudio",
        "ultralytics"
    ]

    run(f"{py} -m pip install " + " ".join(core_packages))

    # --------------------------------------------------
    # 4. Project requirements
    # --------------------------------------------------
    if os.path.exists("requirements.txt"):
        log("STEP 4/5: Installing requirements.txt...")
        run(f"{py} -m pip install -r requirements.txt")
    else:
        log("STEP 4/5: No requirements.txt found → skipping")

    # --------------------------------------------------
    # 5. Sanity check + launch
    # --------------------------------------------------
    log("STEP 5/5: Verifying installation...")
    run(
        f'{py} - <<EOF\n'
        f'import torch, cv2, PyQt5, ultralytics\n'
        f'print("✔ All core modules loaded successfully")\n'
        f'EOF'
    )

    print("\n✅ INSTALLATION COMPLETE")
    print("▶ Launching EthoGrid-ToxMate...\n")

    run(f"{py} main.py")


if __name__ == "__main__":
    main()
