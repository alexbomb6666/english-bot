import os
import telebot
from telebot import types
from gazpacho import get, Soup
from random import choice
import json
with open('db.json', 'r') as file:
  db = json.load(file)
words = {}
def new_account(account, channelid, first_name_db, username_db, preferred_language):
  with open('data.json', 'r') as file:
      user = json.load(file)
  user[username_db] = {
    "username" : username_db,
    "name" : first_name_db,
    "Good tries" : 0, 
    "Bad tries" : 0,
    "IsVIP" : False,
    "IsMod" : False,
    "channelid" : channelid,
    "FreeTries" : 40,
    "blacklisted" : False,
    "language" : preferred_language
  }
  with open("data.json", "w") as write_file:
      json.dump(user, write_file, indent = 4)
token = "2054522973:AAE2VtaZ5ikYFTLt40hTZ-N-fQIsE5KIU6U"
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
  #проверка на существование аккаунта, а если нет, то создать
  try:
    with open('data.json', 'r') as file:
      user = json.load(file)
    usernamed = user[message.chat.username]
  except KeyError:
    #new_account(message.chat.username, message.chat.id, message.chat.first_name, message.chat.username)
    language_tab = types.ReplyKeyboardMarkup(resize_keyboard=True)
    language_tab.row(types.KeyboardButton("Russian/Русский"), types.KeyboardButton("English/Английский"))
    bot.send_message(message.chat.id, f"Привет! На каком языке ты разговариваешь? (Этот параметр пока нельзя будет обновлять сейчас, то есть выбирай с умом) \n Hello! On what language do you speak? (Remember, that parameter can't be changed later for now!", reply_markup = language_tab)
    bot.register_next_step_handler(message, language_check)
    return
  
  if user[message.chat.username]["blacklisted"] == True:
    bot.send_message(message.chat.id, f"Извините, но вы забанены в этом боте. Если вы думаете, что это ошибка, сообщите Ash(er)#4092!")
    return
  #вопрос от бота что нужно
  if user[message.chat.username]["language"] == "russian":
    start_tab = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_tab.row(types.KeyboardButton("Профиль"), types.KeyboardButton("Об боте"), types.KeyboardButton("Лидерборд"))
    start_tab.add(types.KeyboardButton("Учиться"))
    bot.send_message(message.chat.id, f"Привет! Чем я могу помочь? \n \n Для написания команд будучи в основном меню бота, напишите что-нибудь кроме комманд и потом пишите сами команды!", reply_markup = start_tab)
    bot.register_next_step_handler(message, start)
  elif user[message.chat.username]["language"] == "english":
    start_tab = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_tab.row(types.KeyboardButton("Profile"), types.KeyboardButton("About"), types.KeyboardButton("Leaderboard"))
    start_tab.add(types.KeyboardButton("Learn"))
    bot.send_message(message.chat.id, f"Hello! How can i help you? \n \n If you want to write commands, while being at main menu, write something beside commands and write them!", reply_markup = start_tab)
    bot.register_next_step_handler(message, start)
#дополнение к добавлению аккаунта
def language_check(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if message.text == "Russian/Русский":
    new_account(message.chat.username, message.chat.id, message.chat.first_name, message.chat.username, "russian")
    bot.send_message(message.chat.id, f"Ваш язык выставлен на Русский")
  elif message.text == "English/Английский":
    new_account(message.chat.username, message.chat.id, message.chat.first_name, message.chat.username, "english")
    bot.send_message(message.chat.id, f"Your language is set to English")
  else:
    bot.send_message(message.chat.id, f"Нажмите на кнопки ниже вашей клавиатуры!")
    language_tab = types.ReplyKeyboardMarkup(resize_keyboard=True)
    language_tab.row(types.KeyboardButton("Russian/Русский"), types.KeyboardButton("English/Английский"))
    bot.send_message(message.chat.id, f"На каком языке ты разговариваешь? (Этот параметр пока нельзя будет обновлять сейчас, то есть выбирай с умом) \n Hello! On what language do you speak? (Remember, that parameter can't be changed later for now!", reply_markup = language_tab)
    bot.register_next_step_handler(message, language_check)
    return
  hello(message)
def start(message):
  #проверка на бан
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["blacklisted"] == True and user[message.chat.username]["language"] == "russian":
    bot.send_message(message.chat.id, f"Извините, но вы забанены в этом боте. Если вы думаете, что это ошибка, сообщите Ash(er)#4092!")
    return
  elif user[message.chat.username]["blacklisted"] == True and user[message.chat.username]["language"] == "english":
    bot.send_message(message.chat.id, f"Sorry, but you are banned here. Contact Ash(er)#4092 if this is an mistake!")
    return
  #проверка, что написал собственно пользователь
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["language"] == "russian":
    if message.text == "Учиться" and user[message.chat.username]["IsVIP"] == True:
      bot.send_message(message.chat.id, "Вы можете закрыть обучение, написав exit")
      ask(message)
      return
    elif message.text == "Учиться" and user[message.chat.username]["IsVIP"] == False and user[message.chat.username]["FreeTries"] > 0:
      bot.send_message(message.chat.id, "Вы можете закрыть обучение, написав exit")
      ask(message)
      return
    elif message.text == "Учиться" and user[message.chat.username]["IsVIP"] == False  and user[message.chat.username]["FreeTries"] <= 0:
      bot.send_message(message.chat.id, "Твои Free решения закончились, приходи позже или купи VIP у Ash(er)#4092!")
    elif message.text == "Профиль":
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
      bot.send_message(message.chat.id, "Топ 100.")
      def keys(people):
        return people[1]
      lead_people = []
      with open('data.json', 'r') as file:
        user = json.load(file)
      for _ in user:
        lead_people.append([user[_]["username"], user[_]["Good tries"]])
      lead_people.sort(reverse = True, key = keys)
      count = 0
      board = ""
      if len(lead_people) >= 100:
        for _ in range(100):
          board += f"\n {str(count + 1)}. <b>{lead_people[count][0]}</b> с <b>{lead_people[count][1]}</b> правильными решениями"
          count += 1
          if lead_people[count - 1][0] == message.chat.username:
            you = f"Вы, {message.chat.username}, на {count}-ом месте"
      else:
        for _ in range(len(lead_people)):
          board += f"\n {str(count + 1)}. <b>{lead_people[count][0]}</b> с {lead_people[count][1]} правильными решениями "
          count += 1
          if lead_people[count - 1][0] == message.chat.username:
            you = f"Вы, <b>{message.chat.username}</b>, на <b>{count}</b>-ом месте"
      bot.send_message(message.chat.id, board, parse_mode='HTML')
      bot.send_message(message.chat.id, you, parse_mode='HTML')
    else:
      bot.send_message(message.chat.id, "Не понял вас, повторите /start или просто игнорируйте для выхода из основного функционала бота")
      return
    bot.register_next_step_handler(message, start)
  elif user[message.chat.username]["language"] == "english":
    if message.text == "Learn" and user[message.chat.username]["IsVIP"] == True:
      bot.send_message(message.chat.id, "You can leave teaching cycle by pressing 'exit'")
      ask(message)
      return
    elif message.text == "Learn" and user[message.chat.username]["IsVIP"] == False and user[message.chat.username]["FreeTries"] > 0:
      bot.send_message(message.chat.id, "You can leave teaching cycle by pressing 'exit'")
      ask(message)
      return
    elif message.text == "Learn" and user[message.chat.username]["IsVIP"] == False  and user[message.chat.username]["FreeTries"] <= 0:
      bot.send_message(message.chat.id, "Your free learns are out of stock! Go to bot later or contact Ash(er)#4092 to buy VIP or buy more learns!")
    elif message.text == "Profile":
      with open('data.json', 'r') as file:
        user = json.load(file)
      if user[message.chat.username]["IsVIP"] == 0:
        bot.send_message(message.chat.id, f"You are {message.chat.first_name}:\n Main: \n You got {user[message.chat.username]['Good tries']} good guesses;\n Got {user[message.chat.username]['Bad tries']} bad guesses.\n Billing and other: \n Vip is inactive; \n You have {user[message.chat.username]['FreeTries']} free guesses left.")
      else:
        bot.send_message(message.chat.id, f"You are {message.chat.first_name}:\n Main: \n You got {user[message.chat.username]['Good tries']} good guesses;\n Got {user[message.chat.username]['Bad tries']} bad guesses.\n Billing and other: \n Vip is active.")
      if user[message.chat.username]['Good tries'] > user[message.chat.username]['Bad tries']:
        bot.send_message(message.chat.id, "You are doing good! Keep it up!")
      elif user[message.chat.username]['Good tries'] < user[message.chat.username]['Bad tries']:
        bot.send_message(message.chat.id, "Don't work about your mistakes. They will help you reach further goals faster :D")
      elif user[message.chat.username]['Good tries'] == user[message.chat.username]['Bad tries']:
        bot.send_message(message.chat.id, "As one wise man said, 'perfect balance is always wise way to go into perfect future' Keep it up!")
    elif message.text == "About":
      bot.send_message(message.chat.id, "Bot is made by the example of english bot in Coddy. The original maker of the bot is Ash(er)#4092")
    elif message.text == "/start":
      hello(message)
      return
    elif message.text == "Leaderboard":
      bot.send_message(message.chat.id, "Top 100.")
      def keys(people):
        return people[1]
      lead_people = []
      with open('data.json', 'r') as file:
        user = json.load(file)
      for _ in user:
        lead_people.append([user[_]["username"], user[_]["Good tries"]])
      lead_people.sort(reverse = True, key = keys)
      count = 0
      board = ""
      if len(lead_people) >= 100:
        for _ in range(100):
          board += f"\n {str(count + 1)}. <b>{lead_people[count][0]}</b> with <b>{lead_people[count][1]}</b> right guesses"
          count += 1
          if lead_people[count - 1][0] == message.chat.username:
            you = f"You, {message.chat.username}, are on {count}th place"
      else:
        for _ in range(len(lead_people)):
          board += f"\n {str(count + 1)}. <b>{lead_people[count][0]}</b> with <b>{lead_people[count][1]}</b> right guesses"
          count += 1
          if lead_people[count - 1][0] == message.chat.username:
            you = f"You, <b>{message.chat.username}</b>, are on <b>{count}</b>th place"
      bot.send_message(message.chat.id, board, parse_mode='HTML')
      bot.send_message(message.chat.id, you, parse_mode='HTML')
    else:
      bot.send_message(message.chat.id, "Sorry, didnt get you :( say /start")
      return
    bot.register_next_step_handler(message, start)


#the moment when bot starts to ask you about words
def ask(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  global words
  if user[message.chat.username]["language"] == "russian":
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
  elif user[message.chat.username]["language"] == "english":
    id = str(message.chat.id)
    words.setdefault(id, {})
    words[id]['variants'] = [choice(db) for i in range(4)]
    words[id]['answer'] = choice(words[id]['variants'])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    count = 1
    for w in words[id]['variants']:
      if count == 1:
	      item1 = types.KeyboardButton(str(w["rus"]))
      elif count == 2:
        item2 = types.KeyboardButton(str(w["rus"]))
      elif count == 3:
        item3 = types.KeyboardButton(str(w["rus"]))
      elif count == 4:
        item4 = types.KeyboardButton(str(w["rus"]))
      count += 1
    exitting = types.KeyboardButton("***exit***")
    markup.row(item1, item2, item3, item4)
    markup.add(exitting)				
    bot.send_message(message.chat.id, f"What is the translate of {words[id]['answer']['eng']}?", reply_markup=markup)
    bot.register_next_step_handler(message, check)

#checks if the answer is true and gets the points out
def check(message):
  id = str(message.chat.id)
  with open('data.json', 'r') as file:
      user = json.load(file)
  if user[message.chat.username]["language"] == "russian":
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
  elif user[message.chat.username]["language"] == "english":
    if user[message.chat.username]["IsVIP"] == True or user[message.chat.username]["IsMod"] == True or user[message.chat.username]["FreeTries"] > 0:
      if message.text == '***exit***':
        bot.send_message(message.chat.id, "You closed learning down!")
        hello(message)
        return
      if message.text == words[id]['answer']['rus']:
        bot.send_message(message.chat.id, "This is the right answer!")
        with open('data.json', 'r') as file:
          user = json.load(file)
        with open("data.json", "w") as file:
          user[message.chat.username]["Good tries"] += 1
          json.dump(user, file, indent = 4)
      else:
        bot.send_message(message.chat.id, f"Not right! The right answer is: {words[id]['answer']['rus']}")
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
      bot.send_message(message.chat.id, "Your free guesses ended, come back later on contact Ash(er)#4092!")
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
      if message.text[10:] != "all":
        bot.send_message(message.chat.id, "Неправильный ник!")
        return
    global usermod
    usermod = message.text[10:]
    bot.send_message(message.chat.id, "Сколько решений? \n P.S. Для вычитания введите отрицательное число")
    bot.register_next_step_handler(message, howmuch)
  else:
    bot.send_message(message.chat.id, "Ты не модератор!")
def howmuch(message):
  with open('data.json', 'r') as file:
      user = json.load(file)
  if usermod != "all":
    with open("data.json", "w") as file:
        user[usermod]["FreeTries"] += int(message.text)
        json.dump(user, file, indent = 4)
    if int(message.text) > 0:
      bot.send_message(message.chat.id, f"Выдано {user[usermod]['username']} {message.text} решений! У пользователя теперь {user[usermod]['FreeTries']} решений!")
    elif int(message.text) == 0:
      bot.send_message(message.chat.id, f"Вы ввели 0, введите число еще раз")
      bot.register_next_step_handler(message, howmuch)
    elif int(message.text) < 0:
      bot.send_message(message.chat.id, f"Вы убрали {message.text} решений у {usermod}!")
  else:
    with open("data.json", "w") as file:
      for x in user:
        user[x]["FreeTries"] += int(message.text)
      json.dump(user, file, indent = 4)
    if int(message.text) > 0:
      bot.send_message(message.chat.id, f"Всем пользователям выдано {message.text} решений!")
    elif int(message.text) == 0:
      bot.send_message(message.chat.id, f"Вы ввели 0, введите число еще раз")
      bot.register_next_step_handler(message, howmuch)
    elif int(message.text) < 0:
      bot.send_message(message.chat.id, f"Вы убрали {message.text} решений у всех!")
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
#broadcast command
@bot.message_handler(commands = ['broadcast'])
def broadcast(message):
  with open('data.json', 'r') as file:
    user = json.load(file)
  if message.chat.username == "alexbomb6666":
    for _ in user:
      if user[_]["channelid"] != 1084295275:
        bot.send_message(user[_]["channelid"], message.text[11:])
    bot.send_message(message.chat.id, "Сообщение прислано всем!")
bot.polling(none_stop = True)
#https://pythonim.ru/list/metod-sort-python просмотреть