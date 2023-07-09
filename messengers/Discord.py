#!/usr/bin/python

from urllib.request import Request, urlopen
import json


# https://hookdeck.com/webhooks/platforms/how-to-get-started-with-discord-webhooks#how-do-i-add-a-webhook-to-discord
class Discord:
    def __init__(self, webhook: str, botname: str = "April O'Neil",
                 avatarurl: str = "https://i.pinimg.com/originals/87/67/11/876711e56a0ef942cbb2f15844235f2e.jpg"):
        self.webhook = webhook
        if not webhook.startswith("https://discord.com/api/webhooks/"):
            raise RuntimeError(
                "Your webhook should start with https://discord.com/api/webhooks/")
        self.botname = botname
        self.avatar = avatarurl

    def sendmessage(self, message: str):
        data = {
            "username": self.botname,
            "avatar_url": self.avatar,
            "content": message
        }
        req = Request(self.webhook, json.dumps(data).encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        req.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
        response = urlopen(req)
        response.read()
