from telegram import (
    Chat, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update
    )
from telegram.ext import ContextTypes, ConversationHandler
from typing import cast
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.handlers.menu_api_keys import get_api_wb_keys_buttons
from wbsellersnotifierbot.services.notifications import get_all_notifications
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template
    
async def get_bot_instruction(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Возвращает инструкцию по работе с ботом
    '''
    await delete_previous_msg(update, context)
    previously_msg = await send_response(update,
                                         context, 
                                         response=render_template("bot_instruction.j2"),
                                         inline_keyboard=InlineKeyboardMarkup([[keyboards.main_menu]]))
    context.user_data['previously_msg_id'] = previously_msg.message_id
