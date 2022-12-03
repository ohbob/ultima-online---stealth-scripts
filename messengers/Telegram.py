#!/usr/bin/python
import urllib
from urllib.request import Request


# https://core.telegram.org/bots/faq#how-do-i-create-a-bot
# https://techpp.com/2022/01/08/how-to-create-telegram-channel-guide/
# https://neliosoftware.com/content/help/how-do-i-get-the-channel-id-in-telegram/
class Telegram:
    def __init__(self, bottoken: str, channelid: str):
        self.bottoken = bottoken
        self.channelid = channelid

    def sendmessage(self, message: str):
        url = f"https://api.telegram.org/bot{self.bottoken}/sendMessage?" \
              f"chat_id={self.channelid}&text={message.replace(' ', '%20')}"
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        print(response.read().decode('utf-8'))


