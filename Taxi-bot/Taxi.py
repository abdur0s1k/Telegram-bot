import telebot
from telebot import types
import requests

# Замените на ваш токен бота
TOKEN = '7176302534:AAEnN0U0IYhoxBuE_K9l_Ggpvu-kSrHZals'
# Замените на ваш ключ Google Maps API
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

bot = telebot.TeleBot(TOKEN)

# Обработчик команды /taxi
@bot.message_handler(commands=['taxi'])
def send_taxi(message):
    chat_id = message.chat.id
    name = message.from_user.first_name

    # Создаем клавиатуру для отправки локации
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить локацию", request_location=True)
    markup.add(button_geo)

    bot.send_message(chat_id, f"Привет, {name}! Пожалуйста, отправьте вашу локацию, чтобы мы могли вызвать такси.", reply_markup=markup)

# Обработчик получения локации
@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    location = message.location

    # Используйте location.latitude и location.longitude для работы с координатами
    latitude = location.latitude
    longitude = location.longitude

    bot.send_message(chat_id, "Спасибо! Ищем ближайшее такси для вас...")

    # Поиск ближайшего такси с использованием Google Maps API
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{latitude},{longitude}',
        'radius': 5000,  # Радиус поиска в метрах
        'type': 'taxi_stand',  # Поиск мест стоянки такси
        'key': GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    results = response.json().get('results', [])

    if results:
        taxi_place = results[0]
        place_name = taxi_place['name']
        place_address = taxi_place.get('vicinity', 'Адрес не найден')
        bot.send_message(chat_id, f"Ближайшее такси найдено:\nНазвание: {place_name}\nАдрес: {place_address}")
    else:
        bot.send_message(chat_id, "Извините, поблизости не найдено такси.")

    bot.send_photo(chat_id, photo='URL_картинки_машины')  # Замените на URL фото машины

# Запуск бота
bot.polling(none_stop=True)

if __name__ == '__main__':
    bot.polling()
#Ссылка на бота https://t.me/taksa27_bot