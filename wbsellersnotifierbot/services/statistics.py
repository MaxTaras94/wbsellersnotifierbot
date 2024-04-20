from typing import List, Optional
from pydantic import BaseModel, ConfigDict
import httpx
from wbsellersnotifierbot.settings import settings

class StatData(BaseModel):
    orders: int
    sum_orders: int
    sales: int
    sum_sales: int
    refunds: int
    sum_refunds: int

    model_config = ConfigDict(from_attributes=True)

err_msg = {"status": "error", "data": {"text_error": ""}}

async def statistics(tg_user_id: int, key_id: int) -> List[StatData]:
    '''Функция возвращает статистику по заказам/продажам/возвратам пользователей
    '''
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            data = await client.get(settings.url_api_service+f"api/get_statistics/?user_telegram_id={tg_user_id}&key_id={key_id}")     
        return data.json()
    except Exception as e:
        err_msg["text_error"] = e
        return err_msg
