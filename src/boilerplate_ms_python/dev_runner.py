"""
dev_runner.py

This script watches the current directory for any file changes.
When a change is detected, it restarts the Python application with debugpy enabled.
"""

import sys
import subprocess
from watchgod import run_process
from boilerplate_ms_python.config.logger_config import logger


def start_app():
    """
    Starts the Python app using debugpy.
    Replace 'your_app.py' with your actual application's entry point.
    """
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
        logger.info("File changed, restarting app...")


if __name__ == "__main__":
    logger.info("Watching for file changes. Press Ctrl+C to exit.")
    # Watch the current directory (".") and restart the app when any file changes.
    run_process(".", start_app)
