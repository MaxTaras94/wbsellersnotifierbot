import re
from telegram import Chat, Update, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from typing import cast, Union
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers import user_menu
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.services.users import create_user, user
from wbsellersnotifierbot.services.wb_keys import get_wb_keys, remove_wb_key
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template

async def get_api_wb_keys_buttons(update: Update,
                                  context: ContextTypes.DEFAULT_TYPE,
                                  name_menu_section: str):
    '''Возвращает список кнопок с ключами пользователя для заданного меню
    Аргументы:
    name_menu_section -- имя раздела где будут отображаться эти кнопки
    '''
    tg_user_id: int = get_chat_id(update)
    await delete_previous_msg(update, context)
    all_user_keys = await get_api_wb_keys(update, context)
    buttons = []
    if all_user_keys == '':   
        return buttons
    else:
        for key in all_user_keys:
            name = key['api_key'][:10]+"..."+key['api_key'][-10:] if key['name_key'] is None else key['name_key']
            buttons.append([InlineKeyboardButton(name, callback_data=f'{name_menu_section}_{key["id"]}')])
        buttons.append([keyboards.main_menu])
        return buttons
    
async def get_api_wb_keys(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Union[str|dict]:
    '''Функция отправляет пользователю список список его ключей и возвращает соответствующие этому значения типа str
    '''
    query_data = update.callback_query.data
    tg_user_id: int = get_chat_id(update)
    all_user_keys = await get_wb_keys(tg_user_id)
    await delete_previous_msg(update, context)
    if all_user_keys['status'] == 'error':   
        previously_msg = await send_response(update, context, 
                        response=render_template("errors/server_error_for_all_users.j2"),
                        inline_keyboard=keyboards.button_main_menu_markup)
        context.user_data['previously_msg_id'] = previously_msg.message_id
        return ""
    else:
        if len(all_user_keys["data"]) == 0 :
            previously_msg = await send_response(update, 
                                context,
                                response=render_template("api_keys_wb/menu_api_keys_empty.j2"),
                                inline_keyboard=keyboards.api_keys_users_markup_add)
            context.user_data['previously_msg_id'] = previously_msg.message_id
            return ""
        else:
            if query_data == "wb_api_keys":
                previously_msg = await send_response(update, 
                                    context,
                                    response=render_template("api_keys_wb/menu_api_keys.j2", 
                                                              data={"enumerate": enumerate, 
                                                                    "keys":all_user_keys["data"]
                                                                   }
                                                             ),
                                    inline_keyboard=keyboards.api_keys_users_markup_full)
                context.user_data['previously_msg_id'] = previously_msg.message_id
            else:
                return all_user_keys["data"]
    
async def remove_api_wb_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Запрашивает у пользователя информацию по ключу для удаления
    '''
    tg_user_id: int = get_chat_id(update)
    all_user_keys = await get_wb_keys(tg_user_id)
    context.user_data["all_user_keys"] = all_user_keys["data"]
    await delete_previous_msg(update, context)
    if len(all_user_keys["data"]) == 1 :
        previously_msg = await send_response(update, 
                            context,
                            response=render_template("api_keys_wb/request_delete_single_key.j2"),
                            inline_keyboard=keyboards.yes_no_delete_keys_markup)       
        context.user_data["num_key_for_del"] = 1
        context.user_data["previously_msg_id"] = previously_msg.message_id
        return "YES_NO_DECISION_DELETE"
    else:
        previously_msg = await send_response(update, 
                            context,
                            response=render_template("api_keys_wb/request_number_key_for_deletion.j2"),
                            )
        context.user_data["previously_msg_id"] = previously_msg.message_id
        return "GET_NUM_KEY_4_DELETE"

async def get_num_key_from_user_for_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    num_key_for_del = update.message.text
    indexes_of_keys_user = [i[0] for i in enumerate(context.user_data.get("all_user_keys"), 1)]
    await delete_previous_msg(update, context)
    if int(num_key_for_del) not in indexes_of_keys_user:
        previously_msg = await send_response(update, 
                        context,
                        response=render_template("api_keys_wb/key_delition_fail_incorrect_num_key.j2",
                                                  data={"num":num_key_for_del}
                                                 )
                        )
        context.user_data["previously_msg_id"] = previously_msg.message_id
        await delete_previous_msg(update, context)
        previously_msg = await send_response(update, 
                            context,
                            response=render_template("api_keys_wb/menu_api_keys.j2", 
                                                      data={"enumerate": enumerate, 
                                                            "keys":context.user_data.get("all_user_keys")
                                                           }
                                                     ),
                            inline_keyboard=keyboards.api_keys_users_markup_full)
        context.user_data["previously_msg_id"] = previously_msg.message_id
        return ConversationHandler.END
    else:
        context.user_data["num_key_for_del"] = num_key_for_del
        previously_msg = await send_response(update, 
                        context,
                        response=render_template("api_keys_wb/deletion_key.j2",
                                                  data={"num":num_key_for_del}
                                                 ),
                        inline_keyboard=keyboards.yes_no_delete_keys_markup)
        context.user_data["previously_msg_id"] = previously_msg.message_id
        return "YES_NO_DECISION_DELETE"

        
async def confirmation_key_delition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id: int = get_chat_id(update)
    num_key_for_del = context.user_data.get("num_key_for_del")
    id_wb_key_for_wel = context.user_data.get("all_user_keys")[int(num_key_for_del)-1]['id']
    await remove_wb_key(id_wb_key_for_wel)
    await delete_previous_msg(update, context)
    previously_msg = await send_response(update, 
                    context,
                    response=render_template("api_keys_wb/successful_deletion_key.j2",
                                              data={"num":num_key_for_del}
                                             )
                    )
    context.user_data["previously_msg_id"] = previously_msg.message_id
    all_user_keys = await get_wb_keys(tg_user_id)
    await delete_previous_msg(update, context)
    if len(all_user_keys['data']) > 0:         
        previously_msg = await send_response(update, 
                            context,
                            response=render_template("api_keys_wb/menu_api_keys.j2", 
                                                      data={"enumerate": enumerate, 
                                                            "keys":all_user_keys['data']
                                                           }
                                                     ),
                            inline_keyboard=keyboards.api_keys_users_markup_full)
        context.user_data["previously_msg_id"] = previously_msg.message_id
        return ConversationHandler.END
    else:
        previously_msg = await send_response(update, 
                            context,
                            response=render_template("api_keys_wb/menu_api_keys_empty.j2"),
                            inline_keyboard=keyboards.api_keys_users_markup_add
                            )
        context.user_data["previously_msg_id"] = previously_msg.message_id