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
    


def keyboardgen(data_for_gen_keyboard: list) -> InlineKeyboardMarkup:
    keyboard = []
    BUTTON_NOTIFICATION = {"Заказы":"nfcorders",
                           "Продажи":"nfcsales",
                           "Возвраты":"nfcrefunds"
                           }
    for button in data_for_gen_keyboard:
        keyboard.append([InlineKeyboardButton(button[2]+"  " +button[1],
                                              callback_data=f'{BUTTON_NOTIFICATION[button[1]]}_{button[0]}'
                                              )
                        ]
                       )
    keyboard.append([InlineKeyboardButton('Сохранить💾', callback_data='save_new_notific'), keyboards.main_menu])
    return InlineKeyboardMarkup(keyboard)

async def choose_key_for_get_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Возвращает список ключей пользователя для выбора по какому из них настраивать уведомления
    '''
    tg_user_id: int = get_chat_id(update)
    await delete_previous_msg(update, context)
    buttons = await get_api_wb_keys_buttons(update, context, "notifapikey")
    if buttons:
        previously_msg = await send_response(update,
                                             context, 
                                             response=render_template("api_keys_wb/choose_key.j2", data={"section":"настроить уведомления"}),
                                             inline_keyboard=InlineKeyboardMarkup(buttons))
        context.user_data['previously_msg_id'] = previously_msg.message_id

    
async def get_all_notifications_for_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Возвращает список всех активных уведомлений пользователя
    '''
    query = update.callback_query 
    tg_user_id: int = get_chat_id(update)
    key_id = int(query.data.split("_")[1])
    all_notifications = await get_all_notifications(tg_user_id, key_id)
    if all_notifications['status'] == 'error':   
        previously_msg = await send_response(update, context, 
                        response=render_template("errors/server_error_for_all_users.j2"),
                        inline_keyboard=keyboards.button_main_menu_markup)
    else:
        data_for_menu = []
        CHECK = '🟢'
        UNCHECK = '🔴'
        for data in all_notifications['data']:
            type_operation = data['type_operation']
            is_checking = data['is_checking']
            visual_ckeck = CHECK if is_checking else UNCHECK
            data_for_menu.append([data['id'], type_operation, visual_ckeck])
        sorted_data_for_menu = sorted(data_for_menu, key=lambda x: x[1])
        print(f"sorted_data_for_menu = {sorted_data_for_menu}")
        keyboard_markup = keyboardgen(sorted_data_for_menu)
        await delete_previous_msg(update, context)
        previously_msg = await send_response(update, 
                                context,
                                response=render_template("menu_notifications/setting_up_notifications.j2"),
                                inline_keyboard=keyboard_markup)
    context.user_data['previously_msg_id'] = previously_msg.message_id
    