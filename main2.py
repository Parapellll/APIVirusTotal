import telebot
from datetime import datetime
import requests
import time

token = ""
bot = telebot.TeleBot(token)

# Лог файл.
print(bot.get_me())


def log(message, answer):
    print("\n@@")
    print(datetime)
    print(
        "Сообщение от пользователя:\nИмя: {0}\tФамилия: {1}(id: {2})\nТекст:\n{3}".format(message.from_user.first_name,
                                                                                          message.from_user.last_name,
                                                                                          str(message.from_user.id),
                                                                                          message.text))
    for i in range(10): print("-", end='')
    print("\nОтвет бота:")
    print(answer)
    print('\n')



@bot.message_handler(content_types='stickers')
def handle_command_stickers(message):
    answer = "@Ответить пользователю"
    bot.send_message(message.chat.id, "К сожалению я не могу вас понять :(")
    log(message, answer)



@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Обрабатываем и забираем файл.
    answer = "@Получил файл"
    print(message.document.file_id)
    print(bot.get_file(message.document.file_id))
    print(bot.get_file(message.document.file_id).file_path)
    url = 'https://api.telegram.org/file/bot' + token + '/' + str(bot.get_file(message.document.file_id).file_path)

    # Начинается работа с API сервиса VIRTUALTOTAL. Он принимает файл/архив как ссылку, отсюда надо достать ссылку на настоящую проверку файла/архива.
    form = bot.get_file(message.document.file_id).file_path
    form = form[form.find('.') + 1:len(form)]
    destination = 'file.' + form
    print('file: {0} and format: {1}'.format(destination, form))

    params = {'apikey': '', 'url': url}
    response = requests.post('https://www.virustotal.com/vtapi/v2/url/scan', data=params)
    print(response.json())
    bot.send_message(message.chat.id, "Отправил ваш файл на проверку!")
    params = {'apikey': 'bcbe83f8f6a8a54829079f3aee1133435eac480b6c1499dec4452a4a136782f6', 'resource': url}
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "gzip,  My Python requests library example client or username"
    }
    response = requests.post('https://www.virustotal.com/vtapi/v2/url/report',
                             params=params, headers=headers)
    # Прошла ли проверка "ссылки" до самого конца.
    print(response.json())
    if (response.json().get('response_code') == -2 or response.json().get('response_code') == 0):
        count = 0
        while (response.json().get('response_code') != 1):
            time.sleep(20)
            if (count % 5 == 0 and count != 0):
                bot.send_message(message.chat.id,
                                 "Я всё еще проверяю ваш файл...")
            response = requests.post('https://www.virustotal.com/vtapi/v2/url/report', params=params, headers=headers)
            print(response.json().get('response_code'))
            count += 1
    print(response.json())

    # Достаем файл по ссылке(довольно сложная обработка json-файла). Тут идет окончательная проверка нашего файла/архива.
#    end_resource = response.json().get('filescan_id')
 #   end_resource = end_resource[:end_resource.find('')]
  #  params = {'apikey': 'bcbe83f8f6a8a54829079f3aee1133435eac480b6c1499dec4452a4a136782f6',
   #response = requests.get('https://www.virustotal.com/vtapi/v2/file/report',
    #                        params=params, headers=headers)
    # Прошла ли проверка файла/архива до самого конца.
    #print(response.json())
    if (response.json().get('response_code') == -2 or response.json().get('response_code') == 0):
        count = 0
        while (response.json().get('response_code') != 1):
            time.sleep(20)
            if (count % 5 == 0 and count != 0):
                bot.send_message(message.chat.id,
                                 "Я еще проверяю ваш файл...")
            response = requests.post('https://www.virustotal.com/vtapi/v2/file/report', params=params, headers=headers)
            count += 1
    print(response.json())
    # конечный результат 
    if (response.json().get('positives') <= 1):
        bot.send_message(message.chat.id, "В данном файле нет вирусов!!!")
    else:
        bot.send_message(message.chat.id, "Я бы не стал скачивать этот файл:)")
    log(message, answer)



@bot.message_handler(commands=['start'])
def handle_command_start(message):
    answer = "@Отправил клавиатуру"
    use_markup = telebot.types.ReplyKeyboardMarkup(True)
    use_markup.row('/help', '/settings')
    bot.send_message(message.chat.id, "Добро пожаловать! Просто отправьте в меня документ на проверку", reply_markup=use_markup)
    log(message, answer)



@bot.message_handler(commands=['help'])
def handle_command_help(message):
    answer = "@Рассказал про бота"
    bot.send_message(message.chat.id, 'Просто отправьте сюда файл и он будет проверен ботом')
    log(message, answer)



@bot.message_handler(commands=['тыкни меня'])
def handle_command_setting(message):
    bot.send_message(message.chat.id, "я не знаю почему он не работает я устал\n" +
                     "починись")


@bot.message_handler(content_types=['text'])
def handle_command_text(message):
    answer = "@Ответить пользователю"
    bot.send_message(message.chat.id, "К сожалению я не могу вас понять :(")
    log(message, answer)



@bot.message_handler(content_types=['audio'])
def handle_command_audio(message):
    answer = "@Ответить пользователю"
    bot.send_message(message.chat.id, "К сожалению я не могу вас понять :(")
    log(message, answer)


bot.polling(none_stop=True, interval=0)
