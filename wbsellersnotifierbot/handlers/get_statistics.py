import datetime
from telegram import Chat, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from typing import cast
from wbsellersnotifierbot.handlers.delete_message import delete_previous_msg
from wbsellersnotifierbot.handlers.response import get_chat_id, send_response
from wbsellersnotifierbot.handlers.menu_api_keys import get_api_wb_keys_buttons
from wbsellersnotifierbot.keyboards import main_menu, button_main_menu_markup, button_main_menu_markup_and_add_keys
from wbsellersnotifierbot.services.digit_separator import digit_separator
from wbsellersnotifierbot.services.statistics import statistics
from wbsellersnotifierbot.services.wb_keys import get_wb_keys
from wbsellersnotifierbot.templates import render_template


async def choose_key_for_get_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user_id: int = get_chat_id(update)
    await delete_previous_msg(update, context)
    buttons = await get_api_wb_keys_buttons(update, context, "statapikey")
    if buttons:
        previously_msg = await send_response(update,
                                             context, 
                                             response=render_template("api_keys_wb/choose_key.j2", data={"section":"посмотреть статистику"}),
                                             inline_keyboard=InlineKeyboardMarkup(buttons))
        context.user_data['previously_msg_id'] = previously_msg.message_id
    
    
async def getting_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    query = update.callback_query 
    tg_user_id: int = get_chat_id(update)
    key_id = int(query.data.split("_")[1])
    await delete_previous_msg(update, context)
    previously_msg = await send_response(update,
                                         context, 
                                         response=render_template("menu_statistics/statistics_response.j2")
                                        )  
    context.user_data['previously_msg_id'] = previously_msg.message_id
    stat_data = await statistics(tg_user_id, key_id)
    await delete_previous_msg(update, context)
    if stat_data["status"] == "error":
        previously_msg = await send_response(update,
                                         context, 
                                         response=render_template("errors/too_many_req_wb.j2"),
                                         inline_keyboard=button_main_menu_markup
                                        )
    else:
        previously_msg = await send_response(update,
                                         context, 
                                         response=render_template("menu_statistics/statistics.j2",
                                                                  data={'date': datetime.datetime.today().strftime("%d.%m.%Y %H:%M"),
                                                                        'sales': digit_separator(stat_data["data"][0]["sales"]),
                                                                        'sum_sales': digit_separator(stat_data["data"][0]["sum_sales"]),
                                                                        'refunds': digit_separator(stat_data["data"][0]["refunds"]),
                                                                        'sum_refunds': digit_separator(stat_data["data"][0]["sum_refunds"]),
                                                                        'orders': digit_separator(stat_data["data"][0]["orders"]),
                                                                        'sum_orders': digit_separator(stat_data["data"][0]["sum_orders"])
                                                                        }                                                                  
                                                                ),
                                         inline_keyboard=button_main_menu_markup
                                        )
    context.user_data['previously_msg_id'] = previously_msg.message_id