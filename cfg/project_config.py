from dotenv import load_dotenv
import os

load_dotenv()


class ProjectConfig:
    @staticmethod
    def get_token():
        return os.getenv('TOKEN')

    @staticmethod
    def get_api():
        return os.getenv('API_KEY')