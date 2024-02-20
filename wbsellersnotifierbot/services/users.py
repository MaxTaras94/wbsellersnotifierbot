import aiohttp
from typing import List, Optional
from pydantic import BaseModel, ConfigDict
# import httpx
from wbsellersnotifierbot.settings import settings

class UserResponse(BaseModel):
    telegram_id: int
    username: Optional[str]

    model_config = ConfigDict(from_attributes=True)

err_msg = {"status": "error", "data": {"text_error": ""}}

async def users() -> List[UserResponse]:
    '''Функция возвращает список с данными пользователей
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(settings.url_api_service+"api/users/get_users") as users:
                data = await users.json()
        return data
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg
                
async def user(tg_user_id: int) -> List[UserResponse]:
    '''Функция возвращает данные по пользователю
    '''
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(settings.url_api_service+f"api/users/get_user/{tg_user_id}/") as user:
                data = await user.json()
        return data
    except Exception as e:
        err_msg["text_error"] = e 
        return err_msg           

async def create_user(tg_user_id: int,
                      username: Optional[str],
                      source: Optional[str]
                      ) -> List[UserResponse]:
    '''Функция возвращает данные по пользователю после создания записи в БД
    '''
    try:
        async with aiohttp.ClientSession() as client:      
            async with client.post(settings.url_api_service+"api/users/create_user",
                                   json={"telegram_id": tg_user_id,
                                         "username": username,
                                         "source": source}) as response_to_create:
                data = await response_to_create.json()
                status_code = response_to_create.status
        if status_code == 201:
            return data
        else:
            err_msg["text_error"] = data
            return err_msg
    except Exception as e:
        err_msg["text_error"] = e 
        return err_msg 
