from telegram import Update
from telegram.ext import ContextTypes
from luke_thebot.db.model import users_count, set_admin, is_admin
from luke_thebot.bot.permission import user_have_access

async def handler_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.message.from_user.username
    if users_count() == 0:
        set_admin(username)
    
    if not user_have_access(username):
        await update.message.reply_text(f"Your username {username} dont have access to this bot.")
        return

    welcome_msg = (
        "Welcome to Luke The BOT.\n"
        "Send a video link, I will send you the downloaded video back"
    )
    if is_admin(username):
        welcome_msg += "\nYou are ADMIN"

    welcome_msg += "\nCommands list:"
    welcome_msg += "\n/config"

    if is_admin(username):
        welcome_msg += "\n/bot_config"
        welcome_msg += "\n/user_count"
        welcome_msg += "\n/set_admin USERNAME"
        welcome_msg += "\n/unset_admin USERNAME"
        welcome_msg += "\n/add_user USERNAME"
        welcome_msg += "\n/remove_user USERNAME"

    await update.message.reply_text(welcome_msg)