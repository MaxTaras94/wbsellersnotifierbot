# import aiohttp
from datetime import datetime
import httpx
from typing import List, Optional, Union
from wbsellersnotifierbot.settings import settings


err_msg = {"status": "error", "code": "", "data": {"text_error": ""}}

async def get_wb_keys(tg_user_id: int) -> dict:
    '''Функция возвращает список с API ключами пользователей
    '''
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            wb_keys = await client.get(settings.url_api_service+f"api/wb_keys/get_wb_keys/{tg_user_id}/")
        return wb_keys.json()
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg


async def remove_wb_key(wb_key_id: int) -> dict:
    '''Функция удаляет API ключ пользователя
    '''
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            remove_wb_key = await client.delete(settings.url_api_service+f"api/wb_keys/delete_wb_key/{wb_key_id}")
        return remove_wb_key.json()
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg

                
async def check_wb_key(api_key: str) -> dict:
    '''Функция возвращает true/false как результат проверки API ключа
    '''
    
    try:
        async with httpx.AsyncClient(timeout=30) as client: 
            check_wb_key = await client.get(settings.url_wb_for_checking_key,
                                  headers={"Authorization": api_key},
                                  params={'dateFrom':datetime.now().strftime("%Y-%m-%d")}
                                  )
        return {"code": check_wb_key.status_code}
    except Exception as e:
        err_msg["text_error"] = e
        err_msg["code"] = 500
        return err_msg

async def set_wb_key_for_user(tg_user_id: int, api_key: str, name_key: str|None) -> dict:
    '''Функция возвращает данные после создания записи в БД
    '''
    try:
        async with httpx.AsyncClient(timeout=30) as client:     
            set_wb_key_for_user = await client.post(settings.url_api_service+"api/wb_keys/set_wb_key",
                                   json={"user_telegram_id": tg_user_id,
                                           "api_key": api_key,
                                           "name_key": name_key
                                           })
        data = set_wb_key_for_user.json()
        status_code = set_wb_key_for_user.status_code
        if status_code == 201 or status_code == 200:
            return data
        else:
            err_msg["text_error"] = data
            return err_msg
    except httpx.ConnectError as e:
        err_msg["text_error"] = e 
        return err_msg 
