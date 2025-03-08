from telegram import Update
from telegram.ext import ContextTypes
from luke_thebot.db.model import get_user, is_admin, set_admin, create_user, delete_user, user_exists
import re

def extract_command_and_value(message_text):
    # This regex captures the command (letters, digits, underscores)
    # and any argument that may follow separated by whitespace.
    pattern = r'^/(\w+)(?:\s+(.+))?$'
    match = re.match(pattern, message_text)
    if match:
        command = match.group(1)
        value = match.group(2) or ""  # Default to empty string if no value is given.
        return command, value.strip()
    return None, None

async def handler_user_manager(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = get_user(update.message.from_user.username)
    if user is None:
        return
    if not is_admin(user.username):
        return
    cmd, username = extract_command_and_value(update.message.text)
    if not len(username) > 0:
        await update.message.reply_text("Please specify the username")
        return
    
    if cmd == 'set_admin':
        set_admin(username)
        await update.message.reply_text(f"Username {username} is now admin")
        return

    if cmd == 'unset_admin':
        if user_exists(username):
            set_admin(username, False)
        await update.message.reply_text(f"Username {username} is no longer admin")
        return

    if cmd == 'add_user':
        create_user(username)
        await update.message.reply_text(f"Username {username} allowed (created)")
        return
    
    if cmd == 'remove_user':
        delete_user(username)
        await update.message.reply_text(f"Username {username} disallowed (deleted)")
        return

    await update.message.reply_text("No action taken")