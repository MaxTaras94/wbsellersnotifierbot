from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    CommandHandler,    
    filters,
    MessageHandler)
from .menu_api_keys import (
        get_api_wb_keys,
        remove_api_wb_key,
        confirmation_key_delition,
        get_num_key_from_user_for_delete
        )
from .registration_seller import registration_seller, get_api_wb_key_from_user, get_name_api_wb_key_from_user
from .start import start
from .send_message_for_all_users_bot import accept_text_msg, input_text_for_send_msg, sending_message
from .user_menu import user_menu



def create_conv_hand_start() -> ConversationHandler:
    '''Функция возвращает диалог для начала работы с ботом
    Она же поддерживает диалог при первичном добавлении API ключа WB
    '''
    conv_handler_registration = ConversationHandler(
    entry_points=[CommandHandler("start", start), CommandHandler("menu", start),
                  CallbackQueryHandler(registration_seller, pattern="add_new_wb_api_key")],
    states={
        "REGISTRATION": [CallbackQueryHandler(registration_seller, pattern="registration_seller")],
        "GET_API_KEY": [MessageHandler(filters.TEXT, get_api_wb_key_from_user)],
        "GET_API_KEY_NAME": [MessageHandler(filters.TEXT, get_name_api_wb_key_from_user)],
        },
    fallbacks=[CommandHandler("menu", start)],
    )
    return conv_handler_registration
    
def create_conv_hand_remove_api_key() -> ConversationHandler:
    '''Функция возвращает диалог для удаления API ключа WB
    '''
    conv_handler_remove_api_key = ConversationHandler(
    entry_points=[CallbackQueryHandler(remove_api_wb_key, pattern="remove_wb_api_key")],
    states={
        "YES_NO_DECISION_DELETE": [CallbackQueryHandler(confirmation_key_delition, pattern="confirmation_key_delition"),
                                   CallbackQueryHandler(get_api_wb_keys, pattern="wb_api_keys")
                                   ],
        "GET_NUM_KEY_4_DELETE": [MessageHandler(filters.Regex('\d'), get_num_key_from_user_for_delete)],
        },
    fallbacks=[CommandHandler("menu", start)],
    )
    return conv_handler_remove_api_key
    
def create_conv_sending_msg() -> ConversationHandler:
    '''Функция возвращает диалог для начала отправки сообщения всем пользователям бота
    от админов бота
    '''
    conv_handler_sending_msg = ConversationHandler(
    entry_points=[CallbackQueryHandler(input_text_for_send_msg, pattern="send_message_all_users_in_bot")],
    states={
        "ACCEPTTEXTMSG": [MessageHandler(filters.TEXT|filters.Document.ALL|filters.PHOTO, accept_text_msg)],
        "YES_SENDING_MSG": [CallbackQueryHandler(sending_message, pattern="confirmation_sending_msg")],
        },
    fallbacks=[CallbackQueryHandler(user_menu, pattern="menu")],
    )
    return conv_handler_sending_msg