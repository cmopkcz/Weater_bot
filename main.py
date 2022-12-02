#from config import API_KEY_WEATHER
#import datetime
#import aiogram
#import requests


from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import API_KEY
from config import API_KEY_WEATHER
import datetime
import requests
import json, string

bot: Bot = Bot(token=API_KEY)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def start_help(message :types.Message):
    await message.reply('Напиши название города!')

@dp.message_handler()
async def get_weather(message : types.Message):

    code_for_smile = {
        "Clear" : "Ясно \U00002600",
        "Clouds" : "Облачно \U00002601",
        "Rain" : "Дождь \U00002614",
        "Drizzle" : "Дождь \U00002614",
        "Thunderstorm" : "Гроза \U000026A1",
        "Snow" : "Снег \U0001F328",
        "Mist" : "Туман \U0001F32B"
    }

    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&units=metric&APPID={API_KEY_WEATHER}")
        data = r.json()

        name = data["name"]
        current_temp = data["main"]["temp"]
        current_pressure = data["main"]["pressure"]
        current_humidity = data["main"]["humidity"]
        current_visibility = data["visibility"]
        current_wind = data["wind"]["speed"]
        current_sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        current_sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        current_length_day = current_sunset - current_sunrise

        weather_discription = data["weather"][0]["main"]

        if weather_discription in code_for_smile:
            wd = code_for_smile[weather_discription]
        else:
            wd = "Посмотри сам, я не пойму что там!"

        await message.reply(f"****{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***\n"
              f"Погода в: {name}\n"
              f"Температура: {current_temp}°C {wd}\n"
              f"Влажность: {current_humidity}%\n"
              f"Давление: {current_pressure} мм.рт.ст.\n"
              f"Скорость ветра: {current_wind} м/сек\n"
              f"Видимость: {current_visibility} м\n"
              f"Восход солнца: {current_sunrise.time()}\n"
              f"Продолжительность дня: {current_length_day}\n"
              f"Счастливого пути!"
             )

    except Exception as ex:
        await message.reply(message.text)
        await message.reply('Проверь название города')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

