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
    "channelid" : channelid,
    "FreeTries" : 40,
    "blacklisted" : False
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
  #проверка на бан
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["blacklisted"] == True:
    bot.send_message(message.chat.id, f"Извините, но вы забанены в этом боте. Если вы думаете, что это ошибка, сообщите Ash(er)#4092!")
    return
  #проверка на существование аккаунта, а если нет, то создать
  try:
    with open('data.json', 'r') as file:
      user = json.load(file)
    usernamed = user[message.chat.username]
  except KeyError:
    new_account(message.chat.username, message.chat.id, message.chat.first_name, message.chat.username)
  #вопрос от бота что нужно
  start_tab = types.ReplyKeyboardMarkup(resize_keyboard=True)
  start_tab.row(types.KeyboardButton("Профиль"), types.KeyboardButton("Об боте"), types.KeyboardButton("Лидерборд"))
  start_tab.add(types.KeyboardButton("Учиться"))
  bot.send_message(message.chat.id, f"Привет! Чем я могу помочь? \n \n Для написания команд будучи в основном меню бота, напишите что-нибудь и потом пишите!", reply_markup = start_tab)
  bot.register_next_step_handler(message, start)
def start(message):
  #проверка на бан
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["blacklisted"] == True:
    bot.send_message(message.chat.id, f"Извините, но вы забанены в этом боте. Если вы думаете, что это ошибка, сообщите Ash(er)#4092!")
    return
  #проверка, что написал собственно пользователь
  with open('data.json', 'r') as file:
      user = json.load(file)
  if message.text == "Учиться" and user[message.chat.username]["IsVIP"] == True:
    bot.send_message(message.chat.id, "Вы можете закрыть обучение, написав exit")
    ask(message)
    return
  elif message.text == "Учиться" and user[message.chat.username]["IsVIP"] == False and user[message.chat.username]["FreeTries"] > 0:
    bot.send_message(message.chat.id, "Вы можете закрыть обучение, написав exit")
    ask(message)
    return
  elif message.text == "Учиться" and user[message.chat.username]["IsVIP"] == False and user[message.chat.username]["FreeTries"] <= 0:
    bot.send_message(message.chat.id, "Твои Free решения закончились, приходи позже или купи VIP у Ash(er)#4092!")
  elif message.text == "Профиль":
    bot.send_message(message.chat.id, "В разработке!")
    with open('data.json', 'r') as file:
      user = json.load(file)
    if user[message.chat.username]["IsVIP"] == 0:
      bot.send_message(message.chat.id, f"Вы {message.chat.first_name}:\n Основное: \n Прорешали {user[message.chat.username]['Good tries']} раз правильно;\n Прорешали {user[message.chat.username]['Bad tries']} раз неправильно.\n Биллинг и др: \n Вип подписка неактивна; \n У вас {user[message.chat.username]['FreeTries']} бесплатных решений осталось.")
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
    hello(message)
    return
  elif message.text == "Лидерборд":
    bot.send_message(message.chat.id, "В разработке!")
  else:
    bot.send_message(message.chat.id, "Не понял вас, повторите /start или просто игнорируйте для выхода из основного функционала бота")
    return
  bot.register_next_step_handler(message, start)

#the moment when bot starts to ask you about words
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

#checks if the answer is true and gets the points out
def check(message):
  id = str(message.chat.id)
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["IsVIP"] == True or user[message.chat.username]["IsMod"] == True or user[message.chat.username]["FreeTries"] > 0:
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
      bot.send_message(message.chat.id, f"Неверно! Правильный ответ: {words[id]['answer']['eng']}")
      with open('data.json', 'r') as file:
        user = json.load(file)
      with open("data.json", "w") as file:
        user[message.chat.username]["Bad tries"] += 1
        json.dump(user, file, indent = 4)
    ask(message)
    if user[message.chat.username]["IsVIP"] == False and user[message.chat.username]["IsMod"] == False:
      with open("data.json", "w") as file:
          user[message.chat.username]["FreeTries"] -= 1
          json.dump(user, file, indent = 4)
  else:
    bot.send_message(message.chat.id, "Твои Free решения закончились, приходи позже или купи VIP у Ash(er)#4092!")
    hello(message)

#modhelp command
@bot.message_handler(commands = ['modhelp'])
def modhelp(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["IsMod"] == True:
    bot.send_message(message.chat.id, "Команды для модераторов: \n /addtries [username] - добавляет бесплатных решений к аккаунту \n /vip [username] - дает vip аккаунту \n /devip [username] - убирает у игрока vip \n /blacklist [username] - добавить никнейм к заблокированным пользователям \n /whitelist [username] - разблокирует пользователя (противоположно прошлой команде)")
  else:
     bot.send_message(message.chat.id, "Ты не модератор!")

#addtries command
@bot.message_handler(commands = ['addtries'])
def addtries(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["IsMod"] == True:
    try:
      user[message.text[10:]]
    except KeyError:
      bot.send_message(message.chat.id, "Неправильный ник!")
      return
    global usermod
    usermod = message.text[10:]
    bot.send_message(message.chat.id, "Сколько решений?")
    bot.register_next_step_handler(message, howmuch)
  else:
    bot.send_message(message.chat.id, "Ты не модератор!")
def howmuch(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  with open("data.json", "w") as file:
          user[usermod]["FreeTries"] += int(message.text)
          json.dump(user, file, indent = 4)
  bot.send_message(message.chat.id, f"Выдано {user[usermod]['username']} {message.text} решений!")

#vip command
@bot.message_handler(commands = ['vip'])
def vip(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["IsMod"] == True:
    try:
      user[message.text[5:]]
    except KeyError:
      bot.send_message(message.chat.id, "Неправильный ник!")
      return
    global usermod
    usermod = message.text[5:]
    if user[usermod]["IsVIP"] == False:
      with open("data.json", "w") as file:
        user[usermod]["IsVIP"] = True
        json.dump(user, file, indent = 4)
        bot.send_message(message.chat.id, f"VIP в руках {user[usermod]['username']}")
    else:
      bot.send_message(message.chat.id, f"{user[usermod]['username']} уже имеет VIP!")
  else:
    bot.send_message(message.chat.id, "Ты не модератор!")

#devip command
@bot.message_handler(commands = ['devip'])
def devip(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["IsMod"] == True:
    try:
      user[message.text[7:]]
    except KeyError:
      bot.send_message(message.chat.id, "Неправильный ник!")
      return
    global usermod
    usermod = message.text[7:]
    if user[usermod]["IsVIP"] == True:
      with open("data.json", "w") as file:
        user[usermod]["IsVIP"] = False
        json.dump(user, file, indent = 4)
        bot.send_message(message.chat.id, f"VIP убрано у {user[usermod]['username']}!")
    else:
      bot.send_message(message.chat.id, f"У {user[usermod]['username']} уже нет VIP!")
  else:
    bot.send_message(message.chat.id, "Ты не модератор!")

#blacklist command
@bot.message_handler(commands = ['blacklist'])
def blacklist(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["IsMod"] == True:
    try:
      user[message.text[11:]]
    except KeyError:
      bot.send_message(message.chat.id, "Неправильный ник!")
      return
    global usermod
    usermod = message.text[11:]
    if user[usermod]["blacklisted"] == False:
      with open("data.json", "w") as file:
        user[usermod]["blacklisted"] = True
        json.dump(user, file, indent = 4)
        bot.send_message(message.chat.id, f"{user[usermod]['username']} заблокирован!")
    else:
      bot.send_message(message.chat.id, f"У {user[usermod]['username']} уже заблокирован!")
  else:
    bot.send_message(message.chat.id, "Ты не модератор!")

#whitelist command
@bot.message_handler(commands = ['whitelist'])
def whitelist(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["IsMod"] == True:
    try:
      user[message.text[11:]]
    except KeyError:
      bot.send_message(message.chat.id, "Неправильный ник!")
      return
    global usermod
    usermod = message.text[11:]
    if user[usermod]["blacklisted"] == True:
      with open("data.json", "w") as file:
        user[usermod]["blacklisted"] = False
        json.dump(user, file, indent = 4)
        bot.send_message(message.chat.id, f"{user[usermod]['username']} разблокирован!")
    else:
      bot.send_message(message.chat.id, f"У {user[usermod]['username']} уже разблокирован или этот аккаунт не блокировали!")
  else:
    bot.send_message(message.chat.id, "Ты не модератор!")
bot.polling(none_stop = True)