import aiohttp
from datetime import datetime
from typing import List, Optional, Union
from wbsellersnotifierbot.settings import settings


err_msg = {"status": "error", "code": "", "data": {"text_error": ""}}

async def get_wb_keys(tg_user_id: int) -> dict:
    '''Функция возвращает список с API ключами пользователей
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(settings.url_api_service+f"api/wb_keys/get_wb_keys/{tg_user_id}/") as wb_keys:
                data = await wb_keys.json()
        return data
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg


async def remove_wb_key(wb_key_id: int) -> dict:
    '''Функция удаляет API ключ пользователя
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.delete(settings.url_api_service+f"api/wb_keys/delete_wb_key/{wb_key_id}") as remove_wb_key:
                data = await remove_wb_key.json()
        return data
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg

                
async def check_wb_key(api_key: str) -> dict:
    '''Функция возвращает true/false как результат проверки API ключа
    '''
    
    try:
        async with aiohttp.ClientSession() as client: 
            async with client.get(settings.url_wb_for_checking_key,
                                  headers={"Authorization": api_key},
                                  params={'dateFrom':datetime.now().strftime("%Y-%m-%d")}
                                  ) as check_wb_key:
                status_code = check_wb_key.status
        return {"code": status_code}
    except Exception as e:
        err_msg["text_error"] = e
        err_msg["code"] = 500
        return err_msg

async def set_wb_key_for_user(tg_user_id: int, api_key: str, name_key: str|None) -> dict:
    '''Функция возвращает данные после создания записи в БД
    '''
    try:
        async with aiohttp.ClientSession() as client:     
            async with client.post(settings.url_api_service+"api/wb_keys/set_wb_key",
                                   json={"user_telegram_id": tg_user_id,
                                           "api_key": api_key,
                                           "name_key": name_key
                                           }) as set_wb_key_for_user:
                data = await set_wb_key_for_user.json()
                status_code = set_wb_key_for_user.status
        if status_code == 201 or status_code == 200:
            return data
        else:
            err_msg["text_error"] = data
            return err_msg
    except httpx.ConnectError as e:
        err_msg["text_error"] = e 
        return err_msg 
