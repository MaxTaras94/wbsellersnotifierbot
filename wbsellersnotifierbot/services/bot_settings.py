import aiohttp
from datetime import datetime
from typing import List, Optional, Union
import httpx
from wbsellersnotifierbot.settings import settings


async def is_checking_subscription() -> bool:
    '''Функция возвращает из БД False, если проверка подписки не активна, иначе вернёт True
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(settings.url_api_service+f"api/botsettings/get_status_check_subscription/") as check_subscription:
                data = await check_subscription.json()
        return data
    except:
        return {'status': 'error'}

async def update_checking_subscription(data_for_update: List[dict]) -> dict:
    '''Функция обновляет проверку подписки на канал для пользователей в БД 
       В ответ возвращает статус: ок или ошибка
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.post(settings.url_api_service+f"api/botsettings/update_status_check_subscription/",
                                   json=data_for_update) as response:   
                data = await response.json()
        return data
    except:
        return {'status': 'error', 'is_checking': not data_for_update['is_checking']}
