import logging
import json
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import dotenv

dotenv.load_dotenv()

# Get level from .env
ENV_LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

class ProductionJSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "trace_id": getattr(record, "trace_id", "N/A"), 
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

# --- REUSABLE SETUP FUNCTION ---
def setup_logger(logger_name="AppLogger", log_dir="logs"):
    # Create the specific directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(logger_name)
    logger.setLevel(ENV_LOG_LEVEL)

    # Avoid adding multiple handlers if the logger is already setup
    if logger.hasHandlers():
        logger.handlers.clear()

    human_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(human_format)
    logger.addHandler(console_handler)

    # 2. Human File
    human_file = RotatingFileHandler(f"{log_dir}/human.log", maxBytes=5*1024*1024, backupCount=3)
    human_file.setFormatter(human_format)
    logger.addHandler(human_file)

    # 3. JSON File
    json_file = RotatingFileHandler(f"{log_dir}/machine.json", maxBytes=5*1024*1024, backupCount=3)
    json_file.setFormatter(ProductionJSONFormatter())
    logger.addHandler(json_file)

    return logger

# Default logger for main app
log = setup_logger("ProductionLogger", "logs")