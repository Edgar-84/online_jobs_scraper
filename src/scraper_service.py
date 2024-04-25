import os
from datetime import datetime

from src.config.logger_config import logger
from src.config.project_config import project_settings
from src.config.base_config import base_settings
from src.utils.BaseUtils import BaseDirService, BaseFilesService
from src.utils.BaseUtils.base_decorators import working_time
from src.jobs_site import JobsSearchService, ExcelService


class JobsScraperMain:
    START_WORK_MESSAGE = "# ====== START WORKING SCRAPER ======"
    FINISH_WORK_MESSAGE = "# ====== FINISH WORK SCRAPER ======"
    NEED_NEW_COOKIES = "# The COOKIE has expired, you must set new Cookies in the .env file"

    def __init__(self):
        self.jobs_search_service: JobsSearchService = JobsSearchService
        self.site_url = project_settings.site_url
        self.__headers = {
            'User-Agent': project_settings.user_agent,
            'Cookie': project_settings.cookie,
        }
        self.search_job_title: str = None
        self.count_vacancies: int = None
        self.jobs_vacancies_dict: dict = None
        self.excel_status: bool = None
        self.json_status: bool = None

    @classmethod
    def __finish_work_scraper(cls):
        print(cls.FINISH_WORK_MESSAGE)

    def __save_result_to_excel(self):
        dt = datetime.now()
        name_file = os.path.join(
            base_settings.result_files_dir,
            f'{self.search_job_title}_{dt.strftime("%Y-%m-%d_%H-%M-%S")}.xlsx',
        )
        result = ExcelService.create_excel(save_data=self.jobs_vacancies_dict, name_save=name_file)
        return result

    def __save_result_to_json(self):
        dt = datetime.now()
        name_file = os.path.join(
            base_settings.result_files_dir,
            f'{self.search_job_title}_{dt.strftime("%Y-%m-%d_%H-%M-%S")}.json',
        )
        BaseFilesService.dump_json(data_object=self.jobs_vacancies_dict, json_name=name_file)
        return True

    def validate_site_token(self):
        """Check access to site"""
        print("# Starting verification COOKIE...")
        result = self.jobs_search_service.validate_access_to_site(
            url=self.site_url,
            headers=self.__headers,
        )
        if result:
            logger.debug("COOKIE validate successfully")
            print(f"# ====== COOKIE validate successfully for site: {self.site_url} ======")
            return True

        print(self.NEED_NEW_COOKIES)
        return False

    def get_count_vacancies(self) -> bool:
        print("# Check count vacancies ...")
        result = self.jobs_search_service.get_count_vacancies(
            title_job=self.search_job_title,
            site_url=self.site_url,
            headers=self.__headers,
        )

        if result:
            self.count_vacancies = result
            print(f"# ====== Find [{result}] vacancies for: {self.search_job_title} ======")
            return True

        else:
            print(f"# Scraper didn't find vacancies for Job Title: {self.search_job_title}")
            return False

    def get_all_jobs_dict(self) -> bool:
        print("# ====== Start parsing vacancies ======")
        result_jobs = self.jobs_search_service.save_all_vacancies_dict(
            site_url=self.site_url,
            title_job=self.search_job_title,
            headers=self.__headers,
            count_vacancies=self.count_vacancies,
        )
        if result_jobs:
            dt = datetime.now()
            self.jobs_vacancies_dict = result_jobs
            name_file = os.path.join(
                base_settings.temp_dir,
                f'Jobs_{self.search_job_title}_{dt.strftime("%Y-%m-%d_%H-%M-%S")}.json',
            )
            BaseFilesService.dump_json(data_object=self.jobs_vacancies_dict, json_name=name_file)
            return True

        else:
            print("# Mistake during get vacancies information")
            return False

    def save_jobs_to_result_files(self):
        mistake_flag = False

        if self.excel_status:
            excel_res = self.__save_result_to_excel()
            if excel_res is not True:
                mistake_flag = True
                logger.error(f"Wrong result for excel save: {excel_res}")

        if self.json_status:
            json_res = self.__save_result_to_json()
            if json_res is not True:
                mistake_flag = True
                logger.error(f"Wrong result for json save: {json_res}")

        if mistake_flag is False:
            BaseDirService.delete_files_in_temp()

        return True

    @working_time(active=True)
    def main(self, job_title: str, finish_work_func, excel_status: bool, json_status: bool):
        try:
            print(self.START_WORK_MESSAGE)
            self.search_job_title = job_title
            self.excel_status = excel_status
            self.json_status = json_status

            if self.validate_site_token() is False:
                return None

            if self.get_count_vacancies() is False:
                return None

            if self.get_all_jobs_dict() is False:
                return None

            if self.save_jobs_to_result_files() is False:
                return None

        except Exception as ex:
            error_message = f"Catch critical mistake during work SCRAPER: {ex}"
            logger.critical(error_message)
            print(error_message)

        finally:
            finish_work_func()
            self.__finish_work_scraper()
