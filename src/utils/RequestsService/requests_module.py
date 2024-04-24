import time
import requests
from requests import Response

from .base_exceptions import BaseRequestsServiceException
from src.config.logger_config import logger
from src.utils.BaseUtils import BaseInformationService


class BaseRequestsService:
    @staticmethod
    def __base_get_request(url: str,
                           headers: dict = None,
                           params: dict = None,
                           cookies: dict = None) -> Response:
        return requests.get(url=url, headers=headers, params=params, cookies=cookies)

    @classmethod
    def get_request(cls,
                    url: str,
                    headers: dict = None,
                    params: dict = None,
                    cookies: dict = None) -> Response:
        return cls.__base_get_request(url=url, headers=headers, params=params, cookies=cookies)

    # @classmethod
    # def repeatedly_get_request(cls,
    #                            url: str,
    #                            headers: dict = None,
    #                            params: dict = None,
    #                            cookies: dict = None,
    #                            count_repeat_request: int = 5) -> Response | None:
    #     """
    #     :param url: link for request
    #     :param headers: headers for request
    #     :param params: params for request
    #     :param cookies: cookies for request
    #     :param count_repeat_request: count requests if response != ok
    #     :return: Response object or None
    #     """
    #
    #     mistake_pause = 1
    #
    #     try:
    #         logger.info(f"Url: {url}")
    #         response = cls.__base_get_request(url=url, headers=headers, params=params, cookies=cookies)
    #
    #         if response.ok is False:
    #             while mistake_pause != count_repeat_request + 1:
    #                 time.sleep(mistake_pause)
    #                 logger.debug(f"[#{mistake_pause}] Try send request for url: {url}")
    #                 response = cls.__base_get_request(url=url, headers=headers, params=params, cookies=cookies)
    #
    #                 if response.ok is False:
    #                     mistake_pause += 1
    #                     continue
    #
    #                 else:
    #                     return response
    #
    #             error_message = (f"Catch mistake during load url: {url}, status_code: {response.status_code}"
    #                              f"mistake: {response.text}")
    #             logger.warning(error_message)
    #             return None
    #
    #         else:
    #             return response
    #
    #     except BaseRequestsServiceException as ex:
    #         error_message = f"Catch mistake during load url: {url}, mistake: {ex}"
    #         logger.error(error_message)
    #         return None

    @classmethod
    def repeatedly_get_request(cls,
                               url: str,
                               headers: dict = None,
                               params: dict = None,
                               cookies: dict = None,
                               count_repeat_request: int = 5) -> Response | None:
        try:
            session = requests.Session()

            if headers:
                session.headers.update(headers)
            if cookies:
                session.cookies.update(cookies)
            mistake_pause = 1

            for attempt in range(count_repeat_request):
                try:
                    response = session.get(url, params=params, allow_redirects=False)

                    if response.status_code in (301, 302, 303, 307, 308):  # Обработка кодов редиректа.
                        new_url = response.headers['Location']
                        response = session.get(new_url, params=params)

                    if not response.ok:
                        time.sleep(mistake_pause)
                        mistake_pause *= 2
                        continue

                    return response

                except requests.RequestException as e:
                    logger.error(f"Error making request to {url}: {e}")
                    time.sleep(mistake_pause)
                    mistake_pause *= 2

            logger.warning(f"Failed to get a successful response from {url} after {count_repeat_request} attempts.")
            return None

        except BaseRequestsServiceException as ex:
            error_message = f"Catch mistake during load url: {url}, mistake: {ex}"
            logger.error(error_message)
            return None

    @classmethod
    def save_image(cls, url: str, path_save: str) -> bool:
        try:
            response = cls.__base_get_request(url=url)
            with open(path_save, 'wb') as file:
                file.write(response.content)
                return True

        except BaseRequestsServiceException as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return False

    @classmethod
    def save_html_page(cls,
                       text: str,
                       path_save: str) -> bool:
        try:
            with open(path_save, 'w', encoding="utf-8") as file:
                file.write(text)
                return True

        except Exception as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return False
