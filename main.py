import time
import telebot
import subprocess

# Токен вашего бота, полученный от BotFather
TOKEN = '-'

# Создание объекта бота
bot = telebot.TeleBot(TOKEN)

from datetime import datetime

print("Бот в сети\n")
pctime = datetime.now().strftime("%H:%M:%S")

chat_id = None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот для контроля беспроводных точек доступа. Используйте команду /help для получения информаици по всем командам ")
    chat_id = message.chat.id
    main(chat_id,message)

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_start(message):
    response = "Комманды которые может бот испольнять \n"
    response += "/start \n"
    response += "/ping_all - Проверить работоспособность всех роутеров во всех корпусах \n"
    response += "/ping_dg_all - Проверить работоспособность всех роутеров в первом корпусе \n"
    response += "/ping_bt_all - Проверить работоспособность всех роутеров во втором корпусе \n"
    response += "/ping_dg_e - Проверить работоспособность роутеров для сотрудников в первом корпусе \n"
    response += "/ping_dg_s - Проверить работоспособность роутеров для студентов в первом корпусе \n"
    response += "/ping_bt_e - Проверить работоспособность роутеров для сотрудников в втором корпусе \n"
    response += "/ping_bt_s - Проверить работоспособность роутеров для студентов в втором корпусе \n"
    response += "Так же бот может выполнять любые команды написанные на языке интерпретатора командной строки \n"
    bot.reply_to(message, response)

dg_rs_e = ['IP адреса роуетров']
dg_rs_s = ['IP адреса роуетров']

bt_rs_e = ['IP адреса роуетров']
bt_rs_s = ['IP адреса роуетров']

def ping_ar(array,message,dtext):
    response = dtext+"\n"
    for i in range(len(array)):
        with subprocess.Popen(['ping', array[i], '-n','1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) as proc:
            for out in proc.stdout:
                s = out.decode('cp866', 'ignore')  #
                if 'Ответ от' in s:
                    response += f"Роутер {i+1} работает\n"
                elif 'Превышен интервал ожидания для запроса.' in s:
                    response += f"Роутер {i+1} не работает\n"
    bot.reply_to(message, response)

def ping_all(message):
    bot.reply_to(message, "Состояние роутеров на Долгобродской")
    ping_ar(dg_rs_e, message, "Для сотрудников:")
    ping_ar(dg_rs_s, message, "Для студентов:")
    bot.reply_to(message, "Состояние роутеров на Ботанической")
    ping_ar(bt_rs_e, message, "Для сотрудников:")
    ping_ar(bt_rs_s, message, "Для студентов:")

# Обработчик команды /ping_all
@bot.message_handler(commands=['ping_all'])
def handle_start(message):
    ping_all(message)

# Обработчик команды /time
@bot.message_handler(commands=['time'])
def handle_start(message):
    bot.reply_to(message, pctime)

# Обработчик команды /ping_dg_all
@bot.message_handler(commands=['ping_dg_all'])
def handle_start(message):
    bot.reply_to(message, "Рабочее состояние роутеров на Долгобродской")
    ping_ar(dg_rs_e,message,"Для сотрудников:")
    ping_ar(dg_rs_s,message,"Для студентов:")
# Обработчик команды /ping_dg_e
@bot.message_handler(commands=['ping_dg_e'])
def handle_start(message):
    bot.reply_to(message, "Рабочее состояние роутеров для сотрудников на Долгобродской")
    ping_ar(dg_rs_e,message,"Для сотрудников:")
# Обработчик команды /ping_dg_s
@bot.message_handler(commands=['ping_dg_s'])
def handle_start(message):
    bot.reply_to(message, "Рабочее состояние роутеров для сотрудников на Долгобродской")
    ping_ar(dg_rs_s,message,"Для студентов:")

# Обработчик команды /ping_bt_all
@bot.message_handler(commands=['ping_bt_all'])
def handle_start(message):
    bot.reply_to(message, "Состояние роутеров на Ботанической")
    ping_ar(bt_rs_e,message,"Для сотрудников:")
    ping_ar(bt_rs_s,message,"Для студентов:")
# Обработчик команды /ping_bt_e
@bot.message_handler(commands=['ping_bt_e'])
def handle_start(message):
    bot.reply_to(message, "Состояние роутеров на Ботанической")
    ping_ar(bt_rs_e,message,"Для сотрудников:")
# Обработчик команды /ping_bt_s
@bot.message_handler(commands=['ping_bt_s'])
def handle_start(message):
    bot.reply_to(message, "Состояние роутеров на Ботанической")
    ping_ar(bt_rs_s,message,"Для студентов:")

# Обработчик для прочих текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_command(message):
    # Получаем текст сообщения
    command = message.text
    # Выполняем команду в консоли Windows и получаем результат
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='cp866')
        output = result.stdout
        if not output:
            output = "Команда выполнена успешно, но не вернула вывод."
        bot.reply_to(message, output)
    except Exception as e:
        bot.reply_to(message, f"Ошибка при выполнении команды: {str(e)}")


def ping_check(array,dtext,chat_id):
    print("\n")
    for i in range(len(array)):
        with subprocess.Popen(['ping', array[i], '-n','1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) as proc:
            for out in proc.stdout:
                s = out.decode('cp866', 'ignore')
                if 'Ответ от' in s:
                    print(f"Роутер {dtext} {i+1}  работает ")
                elif 'Превышен интервал ожидания для запроса.' in s:
                    bot.send_message(chat_id,  f" Роутер {dtext} {i+1} не работает")

def main(chat_id,message):
    while True:
        #утренне и вечернее извещение о работоспобности роутеров
        if pctime == "08:30:00":
            bot.send_message(chat_id, f" Доброе утро,сейчас {pctime}. Информация роутерам: \n  \n")
            ping_all(message)
        if pctime == "17:30:00":
            bot.send_message(chat_id, f" Добрый вечер,сейчас {pctime}. Информация роутерам: \n  \n")
            ping_all(message)
        ping_check(dg_rs_e, " для сотрудников в первом корпусе",chat_id)
        ping_check(dg_rs_s, " для студентов в первом корпусе",chat_id)
        ping_check(bt_rs_e, " для сотрудников во втором корпусе",chat_id)
        ping_check(bt_rs_s, " для студентов во втором корпусе",chat_id)
        time.sleep (5*60)

bot.polling()
