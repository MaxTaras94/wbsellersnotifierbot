import re
from telegram import Chat, Update 
from telegram.ext import ContextTypes, ConversationHandler
from typing import cast
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.handlers.user_menu import user_menu
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.services.users import create_user, user
from wbsellersnotifierbot.services.wb_keys import check_wb_key, get_wb_keys, set_wb_key_for_user
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template


async def registration_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция внутри диалога GET_API_KEY (модуль create_conv_handkers)
    '''
    await delete_previous_msg(update, context)
    previously_msg = await send_response(update, context, response=render_template("api_keys_wb/request_api_key.j2"))
    context.user_data['previously_msg_id'] = previously_msg.message_id
    return "GET_API_KEY"


async def get_name_api_wb_key_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция внутри диалога GET_API_KEY_NAME (модуль create_conv_handkers)
    '''
    name_api_key_from_user = update.message.text
    tg_user_id: int = get_chat_id(update)
    all_user_keys = await get_wb_keys(tg_user_id)
    wb_api_key_from_user = context.user_data.get('wb_api_key_from_user', None) 
    prohibited_characters = ''
    pattern = re.compile(r'[\\/,\?]')
    check_var = pattern.findall(name_api_key_from_user)
    if check_var:
        previously_msg = await send_response(update, context, response=render_template("errors/error_key_name.j2",
                                                                                        data={"symbol":set(check_var)}))
        context.user_data['previously_msg_id'] = previously_msg.message_id
        return "GET_API_KEY_NAME"    
    else:
        await delete_previous_msg(update, context)
        name_api_key_from_user = None if name_api_key_from_user == "None" else name_api_key_from_user
        if len(all_user_keys["data"]) == 0:
            result = await set_wb_key_for_user(tg_user_id, wb_api_key_from_user, name_api_key_from_user)
            if result['status'] == 'error':
                await delete_previous_msg(update, context)
                previously_msg = await send_response(update, context, 
                                response=render_template("errors/error_saving_key_db.j2"),
                                inline_keyboard=keyboards.menu_users_markup if str(tg_user_id) \
                                not in settings.list_admins else keyboards.menu_admin_markup)
                return ConversationHandler.END
            else:
                previously_msg = await send_response(update, context, response=render_template("api_keys_wb/api_key_correct_and_add_to_user_first.j2"), 
                                inline_keyboard=keyboards.menu_users_markup if str(tg_user_id) \
                                not in settings.list_admins else keyboards.menu_admin_markup)           
            context.user_data['previously_msg_id'] = previously_msg.message_id
            return ConversationHandler.END
        else:
            result = await set_wb_key_for_user(tg_user_id, wb_api_key_from_user, name_api_key_from_user)
            if result['status'] == 'error':   
                await delete_previous_msg(update, context)
                previously_msg = await send_response(update, context, 
                                response=render_template("errors/error_saving_key_db.j2"),
                                inline_keyboard=keyboards.menu_users_markup if str(tg_user_id) \
                                not in settings.list_admins else keyboards.menu_admin_markup)
                
            else:
                previously_msg = await send_response(update, context, response=render_template("api_keys_wb/add_new_api_key.j2"), 
                                inline_keyboard=keyboards.menu_users_markup if str(tg_user_id) \
                                not in settings.list_admins else keyboards.menu_admin_markup)
            context.user_data['previously_msg_id'] = previously_msg.message_id
            return ConversationHandler.END

                                    
async def get_api_wb_key_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция внутри диалога GET_API_KEY (модуль create_conv_handkers)
    '''
    wb_api_key_from_user = update.message.text
    tg_user_id: int = get_chat_id(update)
    match_kirillic_char = re.search(r'[а-яА-Я]', wb_api_key_from_user)
    if "/" in wb_api_key_from_user:
        await user_menu(update, context)
        return ConversationHandler.END
    elif len(wb_api_key_from_user) < 140 or match_kirillic_char is not None:
        previously_msg = await send_response(update, context, response=render_template("errors/api_key_incorrect.j2"))
        context.user_data['previously_msg_id'] = previously_msg.message_id
        return "GET_API_KEY" 
    else:
        await delete_previous_msg(update, context)
        previously_msg = await send_response(update, context, response=render_template("api_keys_wb/checking_api_key.j2"))
        context.user_data['previously_msg_id'] = previously_msg.message_id
        result_of_checking_wb_key = await check_wb_key(wb_api_key_from_user)
        await context.bot.delete_message(tg_user_id, update.message.id) #удаление сообщения с API ключом от пользователя
        if result_of_checking_wb_key['code'] == 401:
            await delete_previous_msg(update, context)
            previously_msg = await send_response(update, context, response=render_template("errors/api_key_invalid.j2"))
            context.user_data['previously_msg_id'] = previously_msg.message_id
            return "GET_API_KEY"
        elif result_of_checking_wb_key['code'] == 429 or result_of_checking_wb_key['code'] == 500:
            await delete_previous_msg(update, context)
            previously_msg = await send_response(update, context, response=render_template("errors/too_many_req_wb.j2"))
            context.user_data['previously_msg_id'] = previously_msg.message_id
            await user_menu(update, context)
            return ConversationHandler.END
        elif result_of_checking_wb_key['code'] == 200:
            await delete_previous_msg(update, context)
            context.user_data['wb_api_key_from_user'] = wb_api_key_from_user
            previously_msg = await send_response(update, context, response=render_template("api_keys_wb/set_name_for_key.j2"))
            context.user_data['previously_msg_id'] = previously_msg.message_id
            return "GET_API_KEY_NAME"