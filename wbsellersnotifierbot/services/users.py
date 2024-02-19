from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import httpx
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
        async with httpx.AsyncClient() as client:      
            data = await client.get(settings.url_api_service+"api/users/get_users")
            return data.json()
    except httpx.ConnectError as e:
        err_msg["text_error"] = e
        return err_msg
                
async def user(tg_user_id: int) -> List[UserResponse]:
    '''Функция возвращает данные по пользователю
    '''
    try:
        async with httpx.AsyncClient() as client:      
            data = await client.get(settings.url_api_service+f"api/users/get_user/{tg_user_id}/")
            return data.json()
    except httpx.ConnectError as e:
        err_msg["text_error"] = e 
        return err_msg           

async def create_user(tg_user_id: int,
                      username: Optional[str],
                      source: Optional[str]
                      ) -> List[UserResponse]:
    '''Функция возвращает данные по пользователю после создания записи в БД
    '''
    try:
        async with httpx.AsyncClient() as client:      
            response = await client.post(settings.url_api_service+"api/users/create_user",
                                     json={"telegram_id": tg_user_id,
                                           "username": username,
                                           "source": source})
        if response.status_code == 201:
            return response.json()
        else:
            err_msg["text_error"] = response.text_error
            return err_msg
    except httpx.ConnectError as e:
        err_msg["text_error"] = e 
        return err_msg 
