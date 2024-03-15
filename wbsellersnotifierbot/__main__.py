from datetime import time
import logging
import pytz
from telegram import Chat, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    CommandHandler,    
    JobQueue,
    MessageHandler,
    filters,
)
import re
from typing import cast
from wbsellersnotifierbot.settings import settings
import wbsellersnotifierbot.handlers as handlers



logging.basicConfig(
    filename="wbbotlogs.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logger = logging.getLogger(__name__)


if not settings.telegram_bot_token:
    raise ValueError(
        "env переменная TELEGRAM_BOT_TOKEN  "
        "не объявлена в .env (должна быть!)"
    )

    
def main():
    '''Функция запуска бота
    '''
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.add_handler(handlers.create_conv_hand_start())
    application.add_handler(handlers.create_conv_sending_msg())
    application.add_handler(handlers.create_conv_hand_remove_api_key())
    application.add_handler(CallbackQueryHandler(handlers.user_menu, pattern="menu"))
    application.add_handler(CallbackQueryHandler(handlers.button_status_click, pattern="nfc"))
    application.add_handler(CallbackQueryHandler(handlers.get_api_wb_keys, pattern="wb_api_keys"))
    application.add_handler(CallbackQueryHandler(handlers.getting_statistics, pattern="statapikey"))
    application.add_handler(CallbackQueryHandler(handlers.save_new_notific, pattern="save_new_notific"))
    application.add_handler(CallbackQueryHandler(handlers.remove_api_wb_key, pattern="remove_wb_api_key"))
    application.add_handler(CallbackQueryHandler(handlers.save_settings, pattern="save_new_check_subscription"))
    application.add_handler(CallbackQueryHandler(handlers.get_all_users_in_bot, pattern="get_all_users_in_bot"))
    application.add_handler(CallbackQueryHandler(handlers.choose_key_for_get_statistics, pattern="statisctics"))
    application.add_handler(CallbackQueryHandler(handlers.get_all_notifications_for_user, pattern="notifapikey"))
    application.add_handler(CallbackQueryHandler(handlers.download_users_xlsx, pattern="download_users_xlsx_button"))
    application.add_handler(CallbackQueryHandler(handlers.choose_key_for_get_notifications, pattern="set_notifications"))
    application.add_handler(CallbackQueryHandler(handlers.button_status_check_subscription, pattern="check_subscription"))
    application.add_handler(CallbackQueryHandler(handlers.get_info_for_checking_subscription, pattern="get_info_for_checking_subscription"))
    
    
    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        logger.warning(traceback.format_exc())
