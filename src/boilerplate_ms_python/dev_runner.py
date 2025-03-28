"""
dev_runner.py

This script watches the current directory for any file changes.
When a change is detected, it restarts the Python application with debugpy enabled.
"""

import sys
import subprocess
from watchgod import run_process


def start_app():
    """
    Starts the Python app using debugpy.
    Replace 'your_app.py' with your actual application's entry point.
    """
    print("Starting application with debugpy (listening on port 5678)...")
    command = [
        sys.executable,
        "-m",
        "debugpy",
        "--listen",
        "5678",  # This flag makes the process wait until a debugger attaches.
        "src/boilerplate_ms_python/main.py",  # TODO: Replace "boilerplate-ms-python" with your project name
    ]
    try:
        subprocess.run(command)
    except KeyboardInterrupt:
        print("Restarting the application...")


if __name__ == "__main__":
    print("Watching for file changes. Press Ctrl+C to exit.")
    # Watch the current directory (".") and restart the app when any file changes.
    run_process(".", start_app)
