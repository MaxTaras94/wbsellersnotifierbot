import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    templates_dir: str = os.getenv("TEMPLATES_DIR", "./templates")
    url_api_service: str = os.getenv("URL_API_SERVICE", "http://localhost")
    url_wb_for_checking_key: str = os.getenv("URL_WB", "https://statistics-api.wildberries.ru/api/v1/supplier/stocks")
    list_admins: list = os.getenv("ADMINS", [])
                

settings = Settings()

