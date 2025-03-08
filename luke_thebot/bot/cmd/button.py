from telegram import Update
from telegram.ext import CallbackContext
from luke_thebot.bot.cmd.config import handler_button as config_handler_button
from luke_thebot.bot.cmd.bot_config import handler_button as bot_config_handler_button

async def handler_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data.startswith('config_bot_'):
        await bot_config_handler_button(update, query)
        return
    if query.data.startswith('config_'):
        await config_handler_button(update, query)
        return