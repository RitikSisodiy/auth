import logging
from datetime import datetime
import json
import traceback

startup_logger = logging.getLogger('database_logger')


def log_startup_info(log_type, data):
    timestamp = datetime.now()
    startup_logger.info(f"{log_type} || {timestamp} || {json.dumps(data)}")
