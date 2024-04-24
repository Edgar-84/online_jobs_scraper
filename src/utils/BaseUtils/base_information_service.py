import inspect

from .base_utils_exceptions import BaseInformationServiceExceptions
from src.config.logger_config import logger


class BaseInformationService:
    """
    Information helper methods
    """
    @staticmethod
    def get_error_message(mistake_message: str) -> str:
        try:
            current_frame = inspect.currentframe()
            outer_frame = inspect.getouterframes(current_frame)
            caller_name = outer_frame[1].function
            error_message = f"Mistake during [{caller_name}]: {mistake_message}"
            return error_message

        except BaseInformationServiceExceptions as ex:
            error_message = "Critical mistake during 'get_error_message"
            logger.error(f"{error_message}: {ex}")
            return error_message
