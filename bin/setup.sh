#!/usr/bin/env bash
set -euo pipefail

echo "**************************************************"
echo " Setting up TDD/BDD Final Project Environment"
echo "**************************************************"

# Keep the system Python untouched. Python 3.9 is used in the original course
# container; local Windows users should follow the PowerShell instructions in README.md.
PYTHON_BIN="${PYTHON_BIN:-python3.9}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Python 3.9 was not found. Install Python 3.9 or set PYTHON_BIN to a compatible interpreter." >&2
    exit 1
fi

"$PYTHON_BIN" --version
"$PYTHON_BIN" -m venv "$HOME/venv"
# shellcheck disable=SC1091
source "$HOME/venv/bin/activate"
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt

if ! command -v chromium >/dev/null 2>&1 && ! command -v google-chrome >/dev/null 2>&1; then
    echo "Chrome/Chromium is required for Selenium BDD tests. Install a supported browser and driver."
fi

if [ ! -f .env ]; then
    cp dot-env-example .env
fi

echo "**************************************************"
echo " Setup complete. Activate with: source ~/venv/bin/activate"
echo " Start service: python run.py"
echo " Run tests: python -m pytest -v"
echo "**************************************************"
