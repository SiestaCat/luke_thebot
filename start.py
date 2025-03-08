import nest_asyncio
import os
from dotenv import load_dotenv
import os
import logging
from luke_thebot.bot.main import main as bot_main, TokenNotSetException
from peewee import SqliteDatabase
from luke_thebot.db.base import db_proxy
from luke_thebot.db.model import User as UserEntity, UserConfig as UserConfigEntity, BotConfig as BotConfigEntity

nest_asyncio.apply()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load .env file variables
load_dotenv()

try:
    # DB
    db = SqliteDatabase(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db', 'sqlite.db'))
    db_proxy.initialize(db)
    db.connect()
    db.create_tables([UserEntity, UserConfigEntity, BotConfigEntity])

    # TG BOT
    main_bot = bot_main(os.getenv("TELEGRAM_TOKEN"))
except TokenNotSetException:
    logger.error("TELEGRAM_TOKEN is not set. Please check your environment or .env file.")
    exit(1)