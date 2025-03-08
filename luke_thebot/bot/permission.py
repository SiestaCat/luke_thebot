from luke_thebot.db.model import user_exists, get_bot_config_value

def user_have_access(username: str) -> bool:
    if get_bot_config_value('allow_to_everyone') or user_exists(username):
        return True
    return False