import asyncio
import telegram
from telegram import Chat, Update 
from telegram.ext import ContextTypes, ConversationHandler
from typing import cast
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.services.users import users
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template

    
async def input_text_for_send_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция отправляет пользователю сообщение о том, что от него ожидается текст для сообщения-рассылки
    '''
    await delete_previous_msg(update, context)
    previously_msg = await send_response(update, 
                                        context,
                                        response=render_template("input_text_for_sending_all_users_bot.j2"),
                                        inline_keyboard=keyboards.button_main_menu_markup)
    context.user_data['previously_msg_id'] = previously_msg.message_id
    return "ACCEPTTEXTMSG"
    
async def accept_text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция текст для сообщения и начинает рассылку по всем пользователям бота при получении подтверждения
    '''
    await delete_previous_msg(update, context)
    tg_user_id: int = get_chat_id(update)
    try:
        id_message_for_sending = update.message.message_id
        chat_id_message_for_sending = update.message.chat_id
    except:
        id_message_for_sending = None
        chat_id_message_for_sending = None
    try:
        photo_id = update.message['photo'][-1]['file_id']
    except IndexError:
        photo_id = None
    if photo_id is not None:      
        context.user_data["photo_id"] = photo_id
        context.user_data["photo_caption"] = update.message.caption         
    else:
        context.user_data["id_message_for_sending"] = id_message_for_sending
        context.user_data["chat_id_message_for_sending"] = chat_id_message_for_sending
    previously_msg = await send_response(update, 
                                            context,
                                            response=render_template("accepting_text_for_sending_msg.j2"),
                                            inline_keyboard=keyboards.yes_no_sending_msg_markup)    
    context.user_data["previously_msg_id"] = previously_msg.message_id
    return "YES_SENDING_MSG"
    
async def sending_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция делает рассылку сообщения всем пользователям бота
    '''
    await delete_previous_msg(update, context)
    tg_user_id: int = get_chat_id(update)   
    list_all_users_in_bot = await users()
    if list_all_users_in_bot['status'] == 'error':   
        previously_msg = await send_response(update, context, 
                        response=render_template("errors/server_error_for_admin.j2"),
                        inline_keyboard=keyboards.button_main_menu_markup)
        context.user_data["previously_msg_id"] = previously_msg.message_id
        return ConversationHandler.END
    else:
        id_message_for_sending = context.user_data.get("id_message_for_sending", None)
        chat_id_message_for_sending = context.user_data.get("chat_id_message_for_sending", None)
        photo_id = context.user_data.get("photo_id", None)
        photo_caption = context.user_data.get("photo_caption", None)
        user_list_forbidden = []
        success_sending = 0      
        for user in list_all_users_in_bot['data']: 
            if user["telegram_id"] == 449441982 or str(user["telegram_id"]) not in settings.list_admins:
                if id_message_for_sending is not None:
                    try:
                        msg = await context.bot.copy_message(chat_id=user["telegram_id"],
                                                               from_chat_id=chat_id_message_for_sending,
                                                               message_id=id_message_for_sending,
                                                               parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
                                                               ) 
                        await context.bot.pin_chat_message(chat_id=user["telegram_id"], message_id=msg.message_id)
                        success_sending += 1
                    except (telegram.error.Forbidden, telegram.error.BadRequest):
                        user_list_forbidden.append(user["telegram_id"])
                    await asyncio.sleep(0.5)
                elif photo_id is not None:
                    try:
                        msg = await context.bot.send_photo(chat_id = user["telegram_id"],
                                                     caption = photo_caption,
                                                     photo = photo_id,
                                                     parse_mode=telegram.constants.ParseMode.HTML)
                        await context.bot.pin_chat_message(chat_id=user["telegram_id"], message_id=msg.message_id)
                        success_sending += 1
                    except (telegram.error.Forbidden, telegram.error.BadRequest):
                        user_list_forbidden.append(user["telegram_id"])
                    await asyncio.sleep(0.5)
        previously_msg = await send_response(update, 
                            context,
                            response=render_template("report_after_sending_msg_for_admin.j2", data={"total": len(list_all_users_in_bot['data']),
                                                                                                    "success_sending": success_sending,
                                                                                                    "blocked_bots": user_list_forbidden,
                                                                                                    "len": len}),
                            inline_keyboard=keyboards.button_main_menu_markup
                            )
        context.user_data["previously_msg_id"] = previously_msg.message_id
        return ConversationHandler.END
