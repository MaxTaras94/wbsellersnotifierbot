from telegram import Chat,  Update
from telegram.ext import ContextTypes
from wbsellersnotifierbot.handlers.response import get_chat_id
    

async def delete_previous_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция удаляет предыдущее сообщение от бота
    '''
    tg_user_id: int = get_chat_id(update)
    previously_msg_id = context.user_data.get('previously_msg_id', 0)
    if previously_msg_id != 0:
        try:
            await context.bot.delete_message(tg_user_id, previously_msg_id)
            del context.user_data['previously_msg_id']
        except Exception as e:
            pass                     