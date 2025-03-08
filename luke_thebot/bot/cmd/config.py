from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes
from luke_thebot.db.model import get_user, get_user_config_value, set_config

def build_config_keyboard(user) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(f"Original video format: {'Yes' if get_user_config_value(user, 'preserve_original_video_format') else 'No'}", callback_data='config_set_preserve_original_video_format')],
        [InlineKeyboardButton(f"Download only video: {'Yes' if get_user_config_value(user, 'download_only_video') else 'No'}", callback_data='config_set_download_only_video')],
        [InlineKeyboardButton(f"Download only photo: {'Yes' if get_user_config_value(user, 'download_only_photo') else 'No'}", callback_data='config_set_download_only_photo')],
    ]
    return InlineKeyboardMarkup(keyboard)

async def handler_config_menu(update: Update, context: ContextTypes.DEFAULT_TYPE = None) -> None:
    user = get_user(update.message.from_user.username)
    if user is None:
        return
    reply_markup = build_config_keyboard(user)
    await update.message.reply_text('My config:', reply_markup=reply_markup)

async def handler_button(update: Update, query: CallbackQuery) -> None:
    user = get_user(update.callback_query.from_user.username)
    if query.data == 'config_set_preserve_original_video_format':
        set_config(user, 'preserve_original_video_format', not get_user_config_value(user, 'preserve_original_video_format'))
    if query.data == 'config_set_download_only_video':
        value = not get_user_config_value(user, 'download_only_video')
        set_config(user, 'download_only_video', value)
        if value == True:
            set_config(user, 'download_only_photo', False)
    if query.data == 'config_set_download_only_photo':
        value = not get_user_config_value(user, 'download_only_photo')
        set_config(user, 'download_only_photo', value)
        if value == True:
            set_config(user, 'download_only_video', False)
    await query.edit_message_reply_markup(reply_markup=build_config_keyboard(user))