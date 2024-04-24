from src.scraper_service import JobsScraperMain
from src.app_interface import AppInterface


def main():
    scraper_main = JobsScraperMain()
    app_interface = AppInterface(scraper_main.main)
    app_interface.run()


if __name__ == "__main__":
    main()
