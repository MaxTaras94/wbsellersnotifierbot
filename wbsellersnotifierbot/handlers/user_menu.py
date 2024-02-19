import asyncio
from .response import get_chat_id, send_response

from telegram import Chat, Update 
from telegram.ext import ContextTypes, ConversationHandler
from typing import cast
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template

async def user_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(1)
    await delete_previous_msg(update, context)
    tg_user_id: int = get_chat_id(update)
    if str(tg_user_id) in settings.list_admins:
        previously_msg = await send_response(update, context, response=render_template("main_menu_admins.j2"), 
                                        inline_keyboard=keyboards.menu_admin_markup)
    else:
        previously_msg = await send_response(update, context, response=render_template("main_menu.j2"), 
                                        inline_keyboard=keyboards.menu_users_markup)
    context.user_data['previously_msg_id'] = previously_msg.message_id
    return ConversationHandler.END