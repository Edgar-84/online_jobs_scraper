import os
from pathlib import Path
from dataclasses import dataclass


BASE_DIR = Path(__file__).resolve().parent.parent.parent


@dataclass
class BaseSettings:
    temp_dir: str
    result_files_dir: str
    logs_dir: str


temp_dir = os.path.join(BASE_DIR, "temp")
result_files_dir = os.path.join(BASE_DIR, "result_files")
logs_dir = os.path.join(BASE_DIR, "logs")


base_settings = BaseSettings(temp_dir, result_files_dir, logs_dir)

