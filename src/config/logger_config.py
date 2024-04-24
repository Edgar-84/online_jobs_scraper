import os
import logging
from datetime import datetime

from src.config.base_config import base_settings


def log_settings():
    """
    Settings for logger
    """

    dt = datetime.now()
    log_filename = os.path.join(base_settings.logs_dir, f'{dt.strftime("%Y-%m-%d")}.log')
    file_log = logging.FileHandler(log_filename, 'a', 'utf-8')
    console_out = logging.StreamHandler()

    file_log.setLevel(logging.DEBUG)
    console_out.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d,%H:%M:%S')
    file_log.setFormatter(formatter)
    console_out.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_log)
    root_logger.addHandler(console_out)
    logging.getLogger("requests").setLevel(logging.WARNING)

    return root_logger


logger = log_settings()
