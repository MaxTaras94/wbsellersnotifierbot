import aiohttp
from datetime import datetime
from typing import List, Optional, Union
from wbsellersnotifierbot.settings import settings


err_msg = {"status": "error", "status_code": "", "data": {"text_error": ""}}

async def get_all_notifications(tg_user_id: int,
                                key_id: int) -> dict:
    '''Функция возвращает статусы уведомлений пользователей из БД
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(settings.url_api_service+f"api/notifications/get_all/?user_telegram_id={tg_user_id}&key_id={key_id}") as notifications:
                data = await notifications.json()
        return data
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg

async def update_notifications(data_for_update: List[dict]) -> dict:
    '''Функция обновляет статусы уведомлений пользователей в БД 
       В ответ возвращает статус: ок или ошибка
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.post(settings.url_api_service+f"api/notifications/update/",
                                   json=data_for_update) as response:   
                data = await response.json()
        return data
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg
