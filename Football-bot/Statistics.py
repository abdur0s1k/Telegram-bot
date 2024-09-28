import telebot
import random
import requests
from datetime import datetime

# Задаем токен бота
TOKEN = "7167717221:AAGH1xBoczXds3iagOkXLaFz7_cBas6SN84"
# Задаем токен для API
API_TOKEN = "a842e04979dc4c618de8cee28c7df49e"

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Список, чтобы хранить уже отправленные матчи
sent_matches = []

# Функция для получения случайных данных о матчах
def get_random_matches():
    # URL для запроса случайных данных о матчах
    url = "https://api.football-data.org/v2/competitions/PL/matches"
    
    headers = {
        'X-Auth-Token': API_TOKEN
    }

    # Запрос данных о матчах
    response = requests.get(url, headers=headers)
    
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Если запрос успешен, получаем JSON-данные
        matches_data = response.json()
        
        # Фильтруем данные и возвращаем случайный матч, который еще не был отправлен
        matches = matches_data['matches']
        available_matches = [match for match in matches if match not in sent_matches]
        
        if available_matches:
            random_match = random.choice(available_matches)
            return random_match
        else:
            # Если нет доступных матчей, возвращаем None
            return None
    else:
        # Если запрос не успешен, возвращаем None
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветственное сообщение при старте
    bot.reply_to(message, "Привет! Я бот, который предоставляет футбольную статистику. Напиши /matches, чтобы получить информацию о рандомных матчах APL.")

# Обработчик команды /matches
@bot.message_handler(commands=['matches'])
def send_matches(message):
    # Получаем случайные данные о матче
    random_match = get_random_matches()
    
    if random_match:
        # Если данные получены успешно
        # Получаем информацию о матче
        home_team = random_match['homeTeam']['name']
        away_team = random_match['awayTeam']['name']
        home_score = random_match['score']['fullTime'].get('homeTeam')
        away_score = random_match['score']['fullTime'].get('awayTeam')
        match_date = random_match['utcDate']

        # Преобразуем время из UTC в читаемый формат
        match_datetime = datetime.strptime(match_date, '%Y-%m-%dT%H:%M:%SZ')
        formatted_date = match_datetime.strftime('%Y-%m-%d %H:%M:%S')

        # Выводим весь ответ для отладки
        print(random_match)
        
        # Проверяем наличие данных о счете
        if home_score is not None and away_score is not None:
            # Формируем сообщение о матче
            match_info = (f"Матч: {home_team} vs {away_team}\n"
                          f"Счет: {home_score} - {away_score}\n"
                          f"Время проведения: {formatted_date} (UTC)")
        else:
            # Если счет недоступен
            match_info = (f"Матч: {home_team} vs {away_team}\n"
                          f"Счет недоступен\n"
                          f"Время проведения: {formatted_date} (UTC)")

        # Отправляем информацию о матче пользователю
        bot.send_message(message.chat.id, match_info)
        
        # Добавляем отправленный матч в список отправленных
        sent_matches.append(random_match)
    else:
        # Если не удалось получить данные о матче, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, "К сожалению, не удалось получить данные о матче или все матчи уже отправлены.")

# Запускаем бота
bot.polling()

#Ссылка на бота https://t.me/Football_statistics27_bot