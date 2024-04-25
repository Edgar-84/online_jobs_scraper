import re
from bs4 import BeautifulSoup

from .base_exceptions import ParsingDataServiceExceptions
from src.config.logger_config import logger
from src.config.project_config import project_settings
from src.utils.BaseUtils.base_information_service import BaseInformationService


class ParsingDataService:
    @staticmethod
    def __get_soup_object(page_data: str, features: str = 'lxml'):
        return BeautifulSoup(markup=page_data, features=features)

    @staticmethod
    def __get_count_records(records_data: str):
        """Get count found vacancies"""

        match = re.search(r'(\d{1,3}(?:,\d{3})?)(?=\+?\s+jobs)', records_data)
        if match:
            number = match.group(0).replace(',', '')
            return number

        else:
            logger.debug(f"Data for parsing count records: {records_data}")
            return 0

    @classmethod
    def get_count_vacancies(cls, page_data: str) -> int | None:
        try:
            soup = cls.__get_soup_object(page_data=page_data)
            count_info = soup.find(class_="results pt-0 pb-0 pl-0 pr-0 pr-md-3 pt-md-4").find(class_="fs-12").text
            logger.debug(f"Count_info: {count_info}")
            count_records = cls.__get_count_records(count_info)
            logger.debug(f"Count_records: {count_records}")
            return int(count_records)

        except ParsingDataServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return None

    @classmethod
    def get_all_vacancies_on_page(cls, page_data: str) -> tuple[list, list] | None:
        """
        Get tuple with list links to vacancies and list title vacancies
        """

        try:
            site_host = project_settings.site_url
            soup = cls.__get_soup_object(page_data=page_data)
            title_text = soup.find_all(class_="fs-16 fw-700")
            logger.debug(f"Count vacancies_title: {len(title_text)}")
            vacancies_title = [data.text for data in title_text]

            links_text = soup.find_all(class_="desc fs-14 d-none d-sm-block")
            logger.debug(f"Count vacancies_links_text: {len(links_text)}")
            vacancies_links = [site_host + data.find('a').get('href') for data in links_text]
            return vacancies_title, vacancies_links

        except ParsingDataServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return None

    @classmethod
    def get_job_description(cls, page_data: str) -> str | None:
        try:
            soup = cls.__get_soup_object(page_data)
            description = soup.find(class_="job-description").text
            return description

        except ParsingDataServiceExceptions as ex:
            error_message = BaseInformationService.get_error_message(ex)
            logger.error(error_message)
            return None
