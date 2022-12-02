import os
import dotenv

#Import API Key for Telegram Bot from enveroment
dotenv.load_dotenv()
API_KEY = os.getenv('API_KEY')
API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
