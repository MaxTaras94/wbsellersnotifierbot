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
from wbsellersnotifierbot.services.bot_settings import is_checking_subscription
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template
    
    
async def get_info_for_checking_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Возвращает инфу о проверке подписки на канал
    '''
    is_checking = await is_checking_subscription()
    if is_checking['status'] == 'error':   
        previously_msg = await send_response(update, context, 
                        response=render_template("errors/server_error_for_admin.j2"),
                        inline_keyboard=keyboards.button_main_menu_markup)
    else:
        data_for_menu = []
        CHECK = '🟢'
        UNCHECK = '🔴'
        type_operation = 'Проверяем' if is_checking['is_checking'] else 'Не проверяем'
        visual_ckeck = CHECK if is_checking['is_checking'] else UNCHECK
        data_for_menu.append([type_operation, visual_ckeck])
        keyboard_markup = keyboards.keyboardgen_for_menu_check_subscription(data_for_menu)
        await delete_previous_msg(update, context)
        previously_msg = await send_response(update, 
                                context,
                                response=render_template("menu_check_subscription.j2"),
                                inline_keyboard=keyboard_markup)
    context.user_data['previously_msg_id'] = previously_msg.message_id
    