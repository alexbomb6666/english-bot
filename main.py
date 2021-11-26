import os
import telebot
from telebot import types
from gazpacho import get, Soup
from random import choice
import json
with open('db.json', 'r') as file:
  db = json.load(file)

words = {}
def new_account(account, channelid, first_name_db, username_db):
  account = {}
  account[username_db] = {
    "username" : username_db,
    "name" : first_name_db,
    "Good tries" : 0, 
    "Bad tries" : 0,
    "IsVIP" : False,
    "IsMod" : False,
    "channelid" : channelid
  }
  with open("data.json", "w") as write_file:
      json.dump(account, write_file, indent = 4)
token = os.environ['token']
bot = telebot.TeleBot(token)
temp = None
def find_website_element(site, where, classes):
    url = site
    html = get(url)
    soup = Soup(html)
    if classes != None:
        return soup.find(where, {'class': classes})
    else:
        return soup.find(where)
@bot.message_handler(commands = ['start'])
def hello(message):
  #bot.send_message(message.chat.id, f"Сегодня {find_website_element('https://yandex.ru', 'div', 'weather__temp').text}")
  #with open('data.json', 'r') as file:
  #  user = json.load(file)
  #if any(x['name'] == message.chat.first_name for x in user) is not True:
  try:
    with open('data.json', 'r') as file:
      user = json.load(file)
    usernamed = user[message.chat.username]
  except KeyError:
    new_account(message.chat.username, message.chat.id, message.chat.first_name, message.chat.username)
  start_tab = types.ReplyKeyboardMarkup(resize_keyboard=True)
  start_tab.row(types.KeyboardButton("Профиль"), types.KeyboardButton("Об боте"), types.KeyboardButton("Лидерборд"))
  start_tab.add(types.KeyboardButton("Учиться"))
  bot.send_message(message.chat.id, f"Привет! Чем я могу помочь?", reply_markup = start_tab)
  bot.register_next_step_handler(message, start)
def start(message):
  if message.text == "Учиться":
    bot.send_message(message.chat.id, "Вы можете закрыть обучение, написав exit")
    ask(message)
    return
  elif message.text == "Профиль":
    bot.send_message(message.chat.id, "В разработке!")
    with open('data.json', 'r') as file:
      user = json.load(file)
    if user[message.chat.username]["IsVIP"] == 0:
      bot.send_message(message.chat.id, f"Вы, {message.chat.first_name}:\n Прорешали {user[message.chat.username]['Good tries']} раз правильно;\n Прорешали {user[message.chat.username]['Bad tries']} раз неправильно;\n Вип подписка неактивна.")
    else:
      bot.send_message(message.chat.id, f"Вы, {message.chat.first_name}:\n Прорешали {user[message.chat.username]['Good tries']} раз правильно;\n Прорешали {user[message.chat.username]['Bad tries']} раз неправильно;\n Вип подписка активна.")
    if user[message.chat.username]['Good tries'] > user[message.chat.username]['Bad tries']:
      bot.send_message(message.chat.id, "Ты хорошо справляешься! Продолжай в том же духе!")
    elif user[message.chat.username]['Good tries'] < user[message.chat.username]['Bad tries']:
      bot.send_message(message.chat.id, "Не беспокойтесь о своих ошибках! Каждая ошибка научит вас новым вещам и тому как их избежать!")
    elif user[message.chat.username]['Good tries'] == user[message.chat.username]['Bad tries']:
      bot.send_message(message.chat.id, "Как сказал один мудрый парень: 'быть в абсолютном балансе - очень хорошая стратегия'. Продолжай в том же духе!")
  elif message.text == "Об боте":
    bot.send_message(message.chat.id, "Бот создан по мотиву экземпляра бота компании Coddy. Индивидуально сделал его я, Ash(er)#4092")
    
  elif message.text == "/start":
    hello()
  elif message.text == "Лидерборд":
    bot.send_message(message.chat.id, "В разработке!")
  else:
    bot.send_message(message.chat.id, "Не понял вас, повторите еще раз.")
  bot.register_next_step_handler(message, start)
def ask(message):
  global words
  id = str(message.chat.id)
  words.setdefault(id, {})
  words[id]['variants'] = [choice(db) for i in range(4)]
  words[id]['answer'] = choice(words[id]['variants'])
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
  count = 1
  for w in words[id]['variants']:
    if count == 1:
	    item1 = types.KeyboardButton(str(w["eng"]))
    elif count == 2:
      item2 = types.KeyboardButton(str(w["eng"]))
    elif count == 3:
      item3 = types.KeyboardButton(str(w["eng"]))
    elif count == 4:
      item4 = types.KeyboardButton(str(w["eng"]))
    count += 1
  exitting = types.KeyboardButton("***exit***")
  markup.row(item1, item2, item3, item4)
  markup.add(exitting)				
  bot.send_message(message.chat.id, f"Какой перевод у слова у {words[id]['answer']['rus']}?", reply_markup=markup)
  bot.register_next_step_handler(message, check)

def check(message):
  id = str(message.chat.id)
  if message.text == '***exit***':
    bot.send_message(message.chat.id, "Вы закрыли обучение!")
    hello(message)
    return
  if message.text == words[id]['answer']['eng']:
    bot.send_message(message.chat.id, "Правильно!")
    with open('data.json', 'r') as file:
      user = json.load(file)
    with open("data.json", "w") as file:
      user[message.chat.username]["Good tries"] += 1
      json.dump(user, file, indent = 4)
  else:
    bot.send_message(message.chat.id, "Неверно!")
    with open('data.json', 'r') as file:
      user = json.load(file)
    with open("data.json", "w") as file:
      user[message.chat.username]["Bad tries"] += 1
      json.dump(user, file, indent = 4)
  ask(message)
bot.polling(none_stop = True)