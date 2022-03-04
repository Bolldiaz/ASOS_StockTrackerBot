import requests
import telebot
import time
import config

HTTP_STATUS = 200
HEADERS = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }
bot = telebot.TeleBot(config.API_KEY)

global RequestFlag
RequestFlag = False


@bot.message_handler(commands=['stop'])
def stop_request(message):
    global RequestFlag
    if not RequestFlag:
        bot.reply_to(message, "No running request session to stop.")
    else:
        bot.reply_to(message, "The tracking has been stopped.")
        RequestFlag = False


def item_request(message):
    request = message.text.splitlines()
    if message == '/stop':
        return False
    elif len(request) != 2:
        bot.reply_to(message, "USAGE to start request:\n"
                              "[ASOS-item-url]\n"
                              "[Desired-size]\n\n"
                              "USAGE to stop request:\n"
                              "[/stop]")
        return False
    # else:
    return True


@bot.message_handler(func=item_request)
def start_request(message):
    global RequestFlag
    bot.reply_to(message, "Start the tracking!")
    url, size = message.text.splitlines()
    try:
        print("####### start-request #######")
        RequestFlag = True
        is_there_model(url, size, message)
    except:
        bot.send_message(message.chat.id, "The code has crashed 🖕")

def is_there_model(url, size_str, message):
    counter = 0
    flag = False
    global RequestFlag
    while RequestFlag:
        page = requests.get(url, headers=HEADERS)
        if page.status_code == HTTP_STATUS:     # ensure the .get was successful
            counter += 1
            if f'"size":"{size_str}","isInStock":true' in page.text:
                flag = True
                bot.reply_to(message, "Back to stock - hurry up!!")
                counter = 0
            time.sleep(1)
            if not flag and counter == 10:
                bot.send_message(message.chat.id, text="Haven't been available for a while, still tracking")
                counter = 0
            time.sleep(1)

bot.polling()
