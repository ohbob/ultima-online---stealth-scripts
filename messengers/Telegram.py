#!/usr/bin/python

# https://core.telegram.org/bots/faq#how-do-i-create-a-bot
# https://techpp.com/2022/01/08/how-to-create-telegram-channel-guide/
# https://neliosoftware.com/content/help/how-do-i-get-the-channel-id-in-telegram/
from urllib.request import urlopen

class Telegram:
    def __init__(self, token: str, channel: str):
        self.url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={channel}&text="

    def send_message(self, message: str):
        print(urlopen(self.url + message.replace(' ', '%20')).read().decode('utf-8'))

#bot = Telegram("bottoken", "chatid")
#bot.send_message("Hello, Telegram!2")
