import os
from dataclasses import dataclass

from dotenv import load_dotenv

from src.config.base_config import BASE_DIR


ENV_FILE_PATH = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=ENV_FILE_PATH)


@dataclass
class ProjectSettings:
    user_agent: dict
    cookie: str
    site_url: str


user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 '
              'Safari/537.36')
cookie = os.getenv('COOKIE')
site_url = 'https://www.onlinejobs.ph'


project_settings = ProjectSettings(user_agent, cookie, site_url)
