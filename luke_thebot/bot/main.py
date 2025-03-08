from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from luke_thebot.bot.cmd.welcome import handler_welcome_message
from luke_thebot.bot.cmd.config import handler_config_menu
from luke_thebot.bot.cmd.bot_config import handler_bot_config_menu
from luke_thebot.bot.cmd.button import handler_button
from luke_thebot.bot.cmd.user_manager import handler_user_manager

class TokenNotSetException(Exception):
    pass

async def handler_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower().startswith() == 'http':
        pass
    await update.message.reply_text("Unknow command to run")

def main(TELEGRAM_TOKEN: str):
    
    if not TELEGRAM_TOKEN:
        raise TokenNotSetException
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", handler_welcome_message))
    app.add_handler(CommandHandler("config", handler_config_menu))
    app.add_handler(CommandHandler("bot_config", handler_bot_config_menu))
    app.add_handler(CommandHandler("set_admin", handler_user_manager))
    app.add_handler(CommandHandler("unset_admin", handler_user_manager))
    app.add_handler(CommandHandler("add_user", handler_user_manager))
    app.add_handler(CommandHandler("remove_user", handler_user_manager))
    app.add_handler(CallbackQueryHandler(handler_button))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_text))

    app.run_polling()