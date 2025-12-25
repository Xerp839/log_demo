import logging
import json
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import dotenv

dotenv.load_dotenv()

# 1. Create logs directory
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()


# 2. The JSON Formatter (For the Machines/TL)
class ProductionJSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            # This captures the 'extra' data like Trace ID
            "trace_id": getattr(record, "trace_id", "N/A"), 
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logger():
    logger = logging.getLogger("ProductionLogger")
    logger.setLevel(LOG_LEVEL)

    # --- FORMAT 1: The Human Format (Pipe Separated) ---
    human_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # --- HANDLER 1: Terminal (Human) ---
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(human_format)
    logger.addHandler(console_handler)

    # --- HANDLER 2: Human File (app.log) ---
    human_file = RotatingFileHandler(f"{LOG_DIR}/app.log", maxBytes=5*1024*1024, backupCount=3)
    human_file.setFormatter(human_format)
    logger.addHandler(human_file)

    # --- HANDLER 3: Machine File (app.json) ---
    json_file = RotatingFileHandler(f"{LOG_DIR}/app.json", maxBytes=5*1024*1024, backupCount=3)
    json_file.setFormatter(ProductionJSONFormatter())
    logger.addHandler(json_file)

    return logger

log = setup_logger()