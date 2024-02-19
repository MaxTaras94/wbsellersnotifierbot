
from telegram import Chat, Update 
from telegram.ext import ContextTypes, ConversationHandler
from typing import cast
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.handlers.user_menu import user_menu
from wbsellersnotifierbot.services.users import user, create_user
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция отправляет приветственное сообщение пользователю бота
    '''
    text_from_start_msg = update.message.text.split(" ")
    source_from_start_msg = text_from_start_msg[-1] if len(text_from_start_msg) > 1 else "" #парсим данные из сообщения /start и забираем текст который передаётся из ссылки
    tg_user_id: int = get_chat_id(update)
    user_ = await user(tg_user_id)
    if str(tg_user_id) in settings.list_admins:
        previously_msg = await send_response(update, context, 
                        response=render_template("main_menu_admins.j2"),
                        inline_keyboard=keyboards.menu_admin_markup)
        context.user_data['previously_msg_id'] = previously_msg.message_id
        if user_['status'] != 'ok':
            await create_user(tg_user_id, update.message.from_user.username, source_from_start_msg)
        return ConversationHandler.END
    elif user_['status'] == 'ok':
        if "start" in text_from_start_msg[0]:
            await send_response(update, context, 
                                response=render_template("start_old_users.j2"),
                                inline_keyboard=keyboards.menu_users_markup)
            return ConversationHandler.END
        else:
            previously_msg = await send_response(update, context, response=render_template("main_menu.j2"), 
                                        inline_keyboard=keyboards.menu_users_markup)
        context.user_data['previously_msg_id'] = previously_msg.message_id
    else:
        await send_response(update, context, 
                            response=render_template("start.j2"),
                            inline_keyboard=keyboards.registration_markup)
        await create_user(tg_user_id, update.message.from_user.username, source_from_start_msg)
        return "REGISTRATION"