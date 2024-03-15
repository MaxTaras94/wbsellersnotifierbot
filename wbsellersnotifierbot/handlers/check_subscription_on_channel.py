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
from wbsellersnotifierbot.services.bot_settings import update_checking_subscription
from wbsellersnotifierbot.settings import settings
from wbsellersnotifierbot.templates import render_template


async def button_status_check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция работает с кнопкой в меню Настройка подписки
        Она обрабатывает события нажатия на кнопку и обновляет на ней текст
    '''
    query = update.callback_query
    check_subscr = {}
    CHECK = '🟢'
    UNCHECK = '🔴'
    name_called_button = query.data
    new_keyboard = []
    for btn in query.message.reply_markup.inline_keyboard:
        if 'save_new_check_subscription' not in btn[0].callback_data and 'menu' not in btn[0].callback_data:
            checked = btn[0].text.startswith(CHECK) #возвращает True, если название кнопки в начале содержит CHECK, иначе вернёт False
            btn_data = btn[0].callback_data
            btn_text = "Проверяем" if not checked else "Не проверяем" 
            if btn_data == name_called_button:
                check_subscr['is_checking'] = not checked
                status = CHECK if not checked else UNCHECK
            else:
                check_subscr['is_checking'] = checked
                status = CHECK if checked else UNCHECK
            new_keyboard.append([btn_text, status])
    context.user_data["check_subscr"] = check_subscr
    previously_msg = await context.bot.edit_message_text(
                                                        chat_id=query.message.chat_id,
                                                        message_id=query.message.message_id,
                                                        text=render_template("menu_check_subscription.j2"),
                                                        reply_markup=keyboards.keyboardgen_for_menu_check_subscription(new_keyboard)
                                                        )
    context.user_data['previously_msg_id'] = previously_msg.message_id   

async def save_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Функция для сохранения проверки подписки
    '''
    check_subscr = context.user_data.get("check_subscr")
    print(f"check_subscr = {check_subscr}")
    results = await update_checking_subscription(check_subscr)
    await delete_previous_msg(update, context)
    if results['status'] == 'ok':
        previously_msg = await send_response(update, 
                                context,
                                response=render_template("save_subscription_status_seccess.j2"
                                                         ),
                            inline_keyboard=keyboards.menu_admin_markup
                            )
        context.user_data['previously_msg_id'] = previously_msg.message_id
    else:
        previously_msg = await send_response(update, 
                                context,
                                response=render_template("errors/error_saving_status_subscribtion.j2"
                                                         ),
                            inline_keyboard=keyboards.menu_admin_markup
                            )
        context.user_data['previously_msg_id'] = previously_msg.message_id