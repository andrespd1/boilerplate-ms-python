import logging
import os

logger = logging.getLogger("bolilerplate_ms_python")

include_line_number = "(%(lineno)d)" if os.getenv("PYTHON_ENV") != "prd" else ""
FORMAT = (
    f"[%(levelname)s] %(asctime)s [%(filename)s](%(funcName)s){include_line_number}: %(message)s"
)
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, LOGGING_LEVEL, logging.INFO),
    format=FORMAT,
)
