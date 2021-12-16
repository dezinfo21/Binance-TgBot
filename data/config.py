from environs import Env

# Используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Токен от вашего бота, которые генерируеться в BotFather
ADMINS = env.list("ADMINS")  # Список админов группы или канала
IP = env.str("ip")  # IP адресс розмещения бота

CHANNEL_ID = env.int("CHANNEL_ID")  # ID вашего телеграм канала, необходим для для удаления постов ботом
TEMP_CHANNEL_ID = env.int("TEMP_CHANNEL_ID")
PUBLIC_CHANNEL_ID = env.int("PUBLIC_CHANNEL_ID")  # ID вашего канала, куда бот будет слать посты для скриншотов
VIEWS_UP_CHANNEL_ID = env.int("VIEWS_UP_CHANNEL_ID")


DB_URI = env.str("DB_URI")  # Строка подключения к базе данных Mongo

API_BASE_URL = env.str("API_BASE_URL")  # Строка запросов к API


API_KEY = env.str("API_KEY")  # Ключ к вашему api в binance
API_SECRET = env.str("API_SECRET")  # Секретный ключ от api в binance

SCREENSHOT_API_KEY = env.str("SCREENSHOT_API_KEY")   # Ключ к скриншот api
