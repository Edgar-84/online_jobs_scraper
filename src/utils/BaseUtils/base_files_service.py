import json

from .base_utils_exceptions import BaseFilesServiceExceptions
from .base_information_service import BaseInformationService
from src.config.logger_config import logger


class BaseFilesService:
    @classmethod
    def dump_json(cls, data_object: dict, json_name: str) -> bool:
        """
        Save json file
        """

        try:
            with open(json_name, "w", encoding='utf-8') as file:
                json.dump(data_object, file, indent=4, ensure_ascii=False)
                return True

        except BaseFilesServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return False

    @classmethod
    def save_html_page(cls, text: str, path_save: str) -> bool:
        try:
            with open(path_save, 'w', encoding="utf-8") as file:
                file.write(text)
                return True

        except BaseFilesServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return False
