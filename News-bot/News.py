import telebot
import requests
import random
from googletrans import Translator

# Задаем токен бота
TOKEN = "6963547249:AAGpAie906j3dmI2MhtP87ReRhUsk2-jFco"

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Функция для получения новостей
def get_news():
    # URL для запроса новостей
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=31f9ff6ba3114e42855ae155adf692e8"
    
    # Отправляем GET-запрос к API новостей
    response = requests.get(url)
    
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Если запрос успешен, преобразуем ответ в JSON и возвращаем
        news = response.json()
        return news
    else:
        # Если запрос не успешен, возвращаем None
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Приветственное сообщение при старте
    bot.reply_to(message, "Привет! Я бот, который выдаёт новости. Напиши /news, чтобы получить новости.")

# Список, чтобы хранить уже отправленные новости
sent_news = []

# Обработчик команды /news
@bot.message_handler(commands=['news'])
def send_news(message):
    # Получаем новости
    news = get_news()
    
    # Проверяем наличие новостей и ключа 'articles' в ответе
    if news and 'articles' in news:
        # Если новости получены и есть статьи
        articles = news['articles']
        
        # Фильтруем статьи, оставляя только те, которые еще не были отправлены
        unsent_articles = [article for article in articles if article not in sent_news]
        
        if unsent_articles:
            # Если остались неотправленные статьи
            # Выбираем случайную статью из неотправленных
            random_article = random.choice(unsent_articles)
            # Получаем заголовок и описание статьи
            title = random_article.get('title', 'No Title')
            description = random_article.get('description', None)  # Обрабатываем None в описании
            
            # Переводим заголовок и описание на русский язык
            translator = Translator()
            title_translated = translator.translate(title, dest='ru').text
            description_translated = translator.translate(description, dest='ru').text if description is not None else 'No Description'  # Обрабатываем None в описании
            
            # Отправляем заголовок и описание статьи пользователю
            bot.send_message(message.chat.id, f"{title_translated}\n{description_translated}")
            
            # Добавляем отправленную статью в список отправленных
            sent_news.append(random_article)
        else:
            # Если все статьи уже отправлены, отправляем сообщение об этом
            bot.send_message(message.chat.id, "Все доступные новости уже были отправлены.")
    else:
        # Если новости не удалось получить, отправляем сообщение об ошибке
        bot.send_message(message.chat.id, "К сожалению, не удалось получить новости.")

# Запускаем бота
bot.polling()

#Ссылка на бота https://t.me/NewsWorldLocal1_bot