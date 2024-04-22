from telegram import Update
from telegram.ext import ContextTypes
from wbsellersnotifierbot import keyboards
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.services.users import users
from wbsellersnotifierbot.templates import render_template


async def unpin_all_messages_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    previously_msg = await send_response(update, context, response=render_template("accept_disable_unpin_all_messages.j2"),
                                         inline_keyboard=keyboards.yes_no_unpin_msg_markup)
    context.user_data['previously_msg_id'] = previously_msg.message_id
    
    
async def unpin_all_messages_accept(update: Update, context: ContextTypes.DEFAULT_TYPE):   
    tg_user_id: int = get_chat_id(update)
    previously_msg_id = context.user_data.get('previously_msg_id', 0)
    await context.bot.delete_message(tg_user_id, previously_msg_id) 
    previously_msg = await send_response(update, context, response=render_template("unpinning_messages.j2"))
    list_all_users_in_bot = await users()
    if list_all_users_in_bot['status'] == 'error':   
        previously_msg = await send_response(update, context, 
                        response=render_template("errors/server_error_for_admin.j2"),
                        inline_keyboard=keyboards.button_main_menu_markup)
        context.user_data["previously_msg_id"] = previously_msg.message_id
    else:
        for user in list_all_users_in_bot['data']:
            try:
                await context.bot.unpin_all_chat_messages(chat_id=user["telegram_id"])
            except:
                pass
        await context.bot.delete_message(tg_user_id, previously_msg.message_id) 
        await send_response(update, context, response=render_template("finish_unpinning.j2"))
