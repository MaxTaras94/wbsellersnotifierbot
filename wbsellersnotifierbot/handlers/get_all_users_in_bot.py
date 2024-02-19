import datetime
import os
import pandas as pd
import telegram
from telegram import Chat, ReplyKeyboardMarkup, Update 
from telegram.ext import ContextTypes
from typing import cast
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.services.users import users
from wbsellersnotifierbot.templates import render_template


async def get_all_users_in_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция для получения всех пользователей бота
    '''
    list_all_users_in_bot = await users()
    await delete_previous_msg(update, context)
    if list_all_users_in_bot['status'] == 'error':   
        previously_msg = await send_response(update, context, 
                        response=render_template("errors/server_error_for_admin.j2"),
                        inline_keyboard=keyboards.button_main_menu_markup)
    else:
        previously_msg = await send_response(update, context, 
                        response=render_template("get_all_users_in_bot.j2", data={"data":len(list_all_users_in_bot['data'])}),
                        inline_keyboard=keyboards.download_users_xlsx_keyboard 
                        )
    context.user_data['previously_msg_id'] = previously_msg.message_id

async def download_users_xlsx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция для выгрузки в .xlsx всех пользователей бота
    '''
    list_all_users_in_bot = await users()
    await delete_previous_msg(update, context)
    tg_user_id: int = cast(Chat, update.effective_chat).id
    if list_all_users_in_bot['status'] == 'error':   
        previously_msg = await send_response(update, context, 
                        response=render_template("errors/server_error_for_admin.j2"),
                        inline_keyboard=keyboards.button_main_menu_markup)
        context.user_data['previously_msg_id'] = previously_msg.message_id
    else:
        today = datetime.datetime.today().strftime("%d.%m.%y %H-%M")
        name_file = f"./all_users_bot_in_db_{today}.xlsx"
        df = pd.DataFrame(list_all_users_in_bot['data'])
        df.to_excel(name_file)
        args = {
                "chat_id": get_chat_id(update),
                "document": name_file,
                "parse_mode": telegram.constants.ParseMode.HTML,
                "reply_markup":keyboards.button_main_menu_markup
            }
        await context.bot.send_document(**args)
        os.remove(name_file)
    