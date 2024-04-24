import os

from .base_utils_exceptions import BaseDirServiceExceptions
from src.config.base_config import base_settings
from src.config.logger_config import logger


class BaseDirService:
    @classmethod
    def delete_files_in_temp(cls, temp_dir: str = base_settings.temp_dir):
        try:
            for filename in os.listdir(temp_dir):
                if filename == '.gitkeep':
                    continue

                file_path = os.path.join(temp_dir, filename)

                if os.path.isfile(file_path):
                    os.remove(file_path)

        except BaseDirServiceExceptions as ex:
            logger.error(f"Mistake during delete files in temp_dir: {temp_dir}, mistake: {ex}")

        logger.debug("Clearing of the Temp directory is finished!")
