import os
import logging


logger = logging.getLogger(
    "bolilerplate_ms_python"
)  # TODO: Replace "boilerplate-ms-python" with your project name

FORMAT = f"[%(levelname)s] %(asctime)s [%(filename)s](%(funcName)s){'(%(lineno)d)' if os.getenv('PYTHON_ENV' )!= 'PRD' else ''}: %(message)s"
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, LOGGING_LEVEL, logging.INFO),
    format=FORMAT,
)
