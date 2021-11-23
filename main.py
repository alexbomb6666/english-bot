import os
import telebot
from telebot import types
from gazpacho import get, Soup
from random import choice
import json
with open('db.json', 'r') as file:
  db = json.load(file)
with open('user_files.json', 'r') as file:
  user = json.load(file)
words = {}
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
  start_tab = types.ReplyKeyboardMarkup(resize_keyboard=True)
  start_tab.row(types.KeyboardButton("Профиль"), types.KeyboardButton("Об боте"))
  start_tab.add(types.KeyboardButton("Учиться"))
  bot.send_message(message.chat.id, "Привет! Чем я могу помочь?", reply_markup = start_tab)
  bot.register_next_step_handler(message, start)
def start(message):
  if message.text == "Учиться":
    bot.send_message(message.chat.id, "Вы можете закрыть обучение, написав exit")
    ask(message)
  elif message.text == "Профиль":
    bot.send_message(message.chat.id, "В разработке!")
    try:
      user[message.chat.username["Good tries"]]
    except KeyError:
      user[message.chat.username["Good tries"]] = 0
      with open('user_files.json', 'r') as file:
        json.dumps(message.chat.username["Good tries"], file)
    bot.send_message(message.chat.id, "Вы всего прорешали " + user[message.chat.username["Good tries"]]+ " успешных опросов!")
    bot.register_next_step_handler(message, start)
  elif message.text == "Об боте":
    bot.send_message(message.chat.id, "Бот создан по мотиву экземпляра бота компании Coddy. Индивидуально сделал его я, Ash(er)#0001")
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
    try:
      user[message.chat.username["Good tries"]]
    except KeyError:
      user[message.chat.username["Good tries"]] = 0
    user[message.chat.username["Good tries"]]+= 1
  else:
    bot.send_message(message.chat.id, "Неверно!")
  ask(message)
bot.polling(none_stop = True)