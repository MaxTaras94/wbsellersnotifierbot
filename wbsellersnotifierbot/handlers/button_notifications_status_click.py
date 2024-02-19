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
from wbsellersnotifierbot.handlers.get_all_notifications import keyboardgen
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.services.notifications import get_all_notifications, update_notifications
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template

from .get_all_notifications import get_all_notifications_for_user

async def button_status_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция работает с кнопками в меню Настройка уведомлений
        Она обрабатывает события нажатия на кнопки и обновляет текст на кнопках
    '''
    query = update.callback_query
    ids_for_change_state = {}
    CHECK = '🟢'
    UNCHECK = '🔴'
    name_called_button, id_button = query.data.split("_")
    new_keyboard = []
    for btn in query.message.reply_markup.inline_keyboard:
        if 'save_new_notific' not in btn[0].callback_data and 'menu' not in btn[0].callback_data:
            checked = btn[0].text.startswith(CHECK) #возвращает True, если название кнопки в начале содержит CHECK, иначе вернёт False
            btn_data, id_ = btn[0].callback_data.split("_")
            btn_text = btn[0].text.replace(f'{UNCHECK} ', '').replace(f'{CHECK} ', '').strip()
            if btn_data == name_called_button:
                ids_for_change_state[int(id_)] = not checked
                status = CHECK if not checked else UNCHECK
            else:
                ids_for_change_state[int(id_)] = checked
                status = CHECK if checked else UNCHECK
            new_keyboard.append([id_, btn_text, status])
    context.user_data["ids_for_change_state"] = ids_for_change_state
    previously_msg = await context.bot.edit_message_text(
                                                        chat_id=query.message.chat_id,
                                                        message_id=query.message.message_id,
                                                        text=render_template("menu_notifications/setting_up_notifications.j2"),
                                                        reply_markup=keyboardgen(new_keyboard)
                                                        )
    context.user_data['previously_msg_id'] = previously_msg.message_id   

async def save_new_notific(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция для сохранения обновлённых настроек уведомлений
    '''
    tg_user_id: int = get_chat_id(update)
    ids_for_change_state = context.user_data.get("ids_for_change_state")
    results = await update_notifications(ids_for_change_state)
    await delete_previous_msg(update, context)
    if results['status'] == 'ok':
        previously_msg = await send_response(update, 
                                context,
                                response=render_template("menu_notifications/save_new_notific.j2"
                                                         ),
                            inline_keyboard=keyboards.menu_users_markup if str(tg_user_id) \
                            not in settings.list_admins else keyboards.menu_admin_markup
                            )
        context.user_data['previously_msg_id'] = previously_msg.message_id
    else:
        previously_msg = await send_response(update, 
                                context,
                                response=render_template("errors/err_save_new_notific.j2"
                                                         ),
                            inline_keyboard=keyboards.menu_users_markup if str(tg_user_id) \
                            not in settings.list_admins else keyboards.menu_admin_markup
                            )
        context.user_data['previously_msg_id'] = previously_msg.message_id