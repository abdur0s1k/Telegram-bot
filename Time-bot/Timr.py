import telebot
import requests

# Задаем токен бота
TOKEN = "6802093130:AAEaseWvpI8BWRtoTTCQUeCvmQNI0GXO2Bk"

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Функция для получения времени по названию города
def get_time_for_city(city_name):
    # Приводим название города к нижнему регистру для соответствия API
    city_name = city_name.lower()
    
    # URL для запроса времени
    url = f"http://worldtimeapi.org/api/timezone/{city_name}"
    
    # Отправляем GET-запрос к API времени
    response = requests.get(url)
    
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Если запрос успешен, преобразуем ответ в JSON и возвращаем время
        data = response.json()
        datetime = data['datetime']
        return datetime
    else:
        # Если запрос не успешен, возвращаем None
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветственное сообщение при старте
    bot.reply_to(message, "Привет! Я бот, который показывает мировое время. Напиши название города, чтобы узнать текущее время в нем.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def send_time(message):
    # Получаем текст сообщения
    city_name = message.text.strip()
    
    # Получаем время для заданного города
    city_time = get_time_for_city(city_name)
    
    if city_time:
        # Если время успешно получено, отправляем его пользователю
        bot.send_message(message.chat.id, f"Текущее время в городе {city_name}: {city_time}")
    else:
        # Если город не найден, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, "Извините, я не знаю такого города. Пожалуйста, введите другой город.")

# Запускаем бота
bot.polling()
#Ссылка на бота https://t.me/Coollers_bot