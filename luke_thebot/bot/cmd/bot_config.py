from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes
from luke_thebot.db.model import get_bot_config_value, set_bot_config, get_user, is_admin, remove_all_users_but_admin

def build_config_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(f"Allow to everyone: {'Yes' if get_bot_config_value('allow_to_everyone') else 'No'}", callback_data='config_bot_set_allow_to_everyone')],
    ]
    return InlineKeyboardMarkup(keyboard)

async def handler_bot_config_menu(update: Update, context: ContextTypes.DEFAULT_TYPE = None) -> None:
    user = get_user(update.message.from_user.username)
    if user is None:
        return
    if not is_admin(user.username):
        return
    await update.message.reply_text('Bot config:', reply_markup=build_config_keyboard())

async def handler_button(update: Update, query: CallbackQuery) -> None:
    user = get_user(update.callback_query.from_user.username)
    if not is_admin(user.username):
        return
    if query.data == 'config_bot_set_allow_to_everyone':
        value = not get_bot_config_value('allow_to_everyone')
        set_bot_config('allow_to_everyone', value)
        if value == False:
            remove_all_users_but_admin()
    await query.edit_message_reply_markup(reply_markup=build_config_keyboard())