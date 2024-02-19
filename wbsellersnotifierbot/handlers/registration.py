import keyboards
from telegram import Chat, InlineKeyboardButton, Update 
from telegram.ext import ContextTypes, ConversationHandler
from typing import cast
from wbsellersnotifierbot.handlers.response import send_response
# from wbsellersnotifierbot.services.check_user_is_admin import is_user_admin
from wbsellersnotifierbot.templates import render_template


async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    previously_msg = await send_response(update, context, 
                        response=render_template("start.j2"),
                        inline_keyboard=keyboards.registration_markup)
    context.user_data['previously_msg_id'] = previously_msg.message_id 
    return ConversationHandler.END