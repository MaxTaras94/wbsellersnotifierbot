from typing import cast, TextIO

import telegram
from telegram import Chat, ReplyKeyboardMarkup, InlineKeyboardMarkup, Message, Update
from telegram.ext import ContextTypes


async def send_response(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    response: str,
    inline_keyboard: InlineKeyboardMarkup | None = None,
    reply_keyboard: ReplyKeyboardMarkup | None = None,
    ) -> Message:
    args = {
        "chat_id": get_chat_id(update),
        "disable_web_page_preview": False,
        "text": response,
        "parse_mode": telegram.constants.ParseMode.HTML,
    }
    if inline_keyboard:
        args["reply_markup"] = inline_keyboard
    elif reply_keyboard:
        args["reply_markup"] = reply_keyboard
    msg = await context.bot.send_message(**args)
    return msg


def get_chat_id(update: Update) -> int:
    return cast(Chat, update.effective_chat).id
