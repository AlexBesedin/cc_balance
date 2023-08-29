import os
import telebot
from dotenv import load_dotenv
from tronpy.providers import HTTPProvider
from tronpy import Tron
from tronpy.keys import PrivateKey

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TRX_PRIVATE_KEY = os.getenv('TRX_PRIVATE_KEY')
TRX_WALLET = os.getenv('TRX_WALLET')
API_KEY = os.getenv('API_KEY')

priv_key = PrivateKey(bytes.fromhex(TRX_PRIVATE_KEY))

bot = telebot.TeleBot(TELEGRAM_TOKEN)

provider = HTTPProvider(api_key=API_KEY)
client = Tron(provider)