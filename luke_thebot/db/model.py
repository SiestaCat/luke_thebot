from peewee import BooleanField, ForeignKeyField, DoesNotExist, CharField, DateTimeField
from luke_thebot.db.base import BaseModel
import datetime
import os

DEFAULT_PRESERVE_ORIGINAL_VIDEO_FORMAT = False
DEFAULT_DOWNLOAD_ONLY_VIDEO = False
DEFAULT_DOWNLOAD_ONLY_PHOTO = False

# USER

class User(BaseModel):
    username = CharField(unique=True)
    is_admin = BooleanField(default=False)
    created_date = DateTimeField(default=datetime.datetime.now)

def get_user(username: str) -> User | None:
    try:
        return User.get(User.username == username)
    except DoesNotExist:
        return None

def user_exists(username: str) -> bool:
    return not get_user(username) is None

def is_admin(username: str) -> bool:
    user = get_user(username)
    if not user is None:
        return user.is_admin
    return False

def set_admin(username: str, is_admin: bool = True) -> None:
    if is_admin and not user_exists(username):
        create_user(username)
    user = get_user(username)
    if not user is None:
        user.is_admin = is_admin
        user.save()

def create_user(username: str) -> None:
    if not user_exists(username):
        User.create(username=username)
        create_config(get_user(username))

def delete_user(username: str) -> None:
    if user_exists(username):
        User.get(User.username == username).delete_instance()

def users_count() -> int:
    return User.select().count()

def remove_all_users_but_admin() -> None:
    for user in User.select().where(User.is_admin == False):
        user.delete_instance()

# USER CONFIG

class UserConfig(BaseModel):
    user = ForeignKeyField(User, backref='config')
    preserve_original_video_format = BooleanField(default=DEFAULT_PRESERVE_ORIGINAL_VIDEO_FORMAT)
    download_only_video = BooleanField(default=DEFAULT_DOWNLOAD_ONLY_VIDEO)
    download_only_photo = BooleanField(default=DEFAULT_DOWNLOAD_ONLY_PHOTO)

def get_user_config(user: User) -> UserConfig:
    if not config_exists(user):
        create_config(user)
    return user.config[0]

def config_exists(user: User) -> bool:
    return len(user.config) > 0

def create_config(user: User) -> None:
    if not config_exists(user):
        UserConfig.create(user=user)

def set_config(user: User, field, value) -> None:
    config = get_user_config(user)
    setattr(config, field, value)
    config.save()

def get_user_config_value(user: User, field):
    config = get_user_config(user)
    return getattr(config, field)

# CONFIG

class BotConfig(BaseModel):
    allow_to_everyone = BooleanField(default=lambda: os.getenv("ALLOW_TO_EVERYONE") == '1')

def get_bot_config() -> BotConfig:
    if not bot_config_exists():
        BotConfig.create()
    return BotConfig.get()

def bot_config_exists() -> bool:
    return BotConfig.select().count() > 0

def set_bot_config(field, value) -> None:
    config = get_bot_config()
    setattr(config, field, value)
    config.save()

def get_bot_config_value(field):
    config = get_bot_config()
    return getattr(config, field)
