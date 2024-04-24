import math

from requests import Response

from .base_exceptions import JobsSearchServiceExceptions
from .parsing_data_service import ParsingDataService
from src.utils.BaseUtils.base_decorators import working_time
from src.utils.BaseUtils import BaseInformationService, BaseFilesService
from src.config.logger_config import logger
from src.utils.RequestsService.requests_module import BaseRequestsService
from src.config.base_config import base_settings


class JobsSearchService:
    JOB_SEARCH_PAGE_PREFIX = '/jobseekers/jobsearch'

    @staticmethod
    def client_message(message: str):
        print(message)
        logger.info(message)

    @classmethod
    def validate_access_to_site(cls, url: str, headers: dict) -> bool:
        """Check validation from work with requests for site"""
        result = BaseRequestsService.repeatedly_get_request(url=url, headers=headers)
        if result is None:
            return None

        else:
            return result.ok

    @classmethod
    @working_time(active=True)
    def save_all_vacancies_dict(cls,
                                site_url: str,
                                title_job: str,
                                headers: dict,
                                count_vacancies: int) -> None | dict:
        try:
            final_result_info = dict()
            number_record = 1
            url = site_url + cls.JOB_SEARCH_PAGE_PREFIX
            iteration_index = 30
            count_pages = math.ceil(count_vacancies / iteration_index)
            cls.client_message(f"# Find {count_pages} pages")
            page_index = 0

            for page in range(count_pages):
                cls.client_message(f"# Get info for page #[{page + 1}] ...")
                url_with_pagination = url + f"/{page_index}"
                page_index += iteration_index

                result_page = cls.get_search_page(
                    title_job=title_job,
                    site_url=url_with_pagination,
                    headers=headers,
                )

                if result_page:
                    cls.client_message(f"# Get vacancies for page #[{page + 1}]")
                    vacancies_data = ParsingDataService.get_all_vacancies_on_page(result_page.text)

                    if vacancies_data is None:
                        logger.critical(f"Mistake during get vacancies for page #[{page}], url: {url_with_pagination}")
                        return None

                    else:
                        vacancies_title, vacancies_links = vacancies_data
                        if len(vacancies_title) != len(vacancies_links):
                            logger.critical(f"Different count title and links: links: {len(vacancies_links)}, "
                                            f"{len(vacancies_title)}")
                            return None

                    vacancies_description = cls._get_descriptions_list(
                        vacancies_links=vacancies_links,
                        headers=headers,
                        page=page+1
                    )
                    if vacancies_description is None:
                        logger.critical("Mistake during getting vacancies description")
                        return None

                    for item in range(len(vacancies_description)):
                        final_result_info[number_record] = {
                            'Job Title': vacancies_title[item],
                            'Link': vacancies_links[item],
                            'Description': vacancies_description[item],
                        }
                        number_record += 1

                else:
                    logger.warning(f"Didn't download page: {url_with_pagination}")
                    return None

            return final_result_info

        except JobsSearchServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return None

    @classmethod
    @working_time(active=True)
    def get_search_page(cls,
                        title_job: str,
                        site_url: str,
                        headers: dict) -> None | Response:
        try:
            params = {'jobkeyword': title_job}
            response = BaseRequestsService.repeatedly_get_request(url=site_url, params=params, headers=headers)

            if response is None:
                return None

            else:
                return response

        except JobsSearchServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.critical(error_message)

    @classmethod
    def get_count_vacancies(cls,
                            title_job: str,
                            site_url: str,
                            headers: dict) -> None | int:
        try:
            url = site_url + cls.JOB_SEARCH_PAGE_PREFIX
            result = cls.get_search_page(title_job=title_job, site_url=url, headers=headers)

            if result:
                count_vacancies = ParsingDataService.get_count_vacancies(result.text)
                return count_vacancies

            else:
                return None

        except JobsSearchServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.critical(error_message)

    @classmethod
    def _get_descriptions_list(cls, vacancies_links: list, headers: dict, page: int) -> None | list:
        try:
            result_links = []

            for number, link in enumerate(vacancies_links):
                response = BaseRequestsService.repeatedly_get_request(url=link, headers=headers)

                if response is None:
                    logger.error(f"Mistake getting information from page: {link}")
                    return None

                else:
                    description = ParsingDataService.get_job_description(response.text)
                    if description is None:
                        logger.error(f"Mistake getting description for: {link}")
                        return None

                    else:
                        result_links.append(description)
                        cls.client_message(f"# Save information from #{number + 1} job, for page [{page}]")

            return result_links

        except JobsSearchServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.critical(error_message)
            return None
