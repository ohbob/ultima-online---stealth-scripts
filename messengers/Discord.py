#!/usr/bin/python

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json

class Discord:
    def __init__(self, webhook: str, botname: str = "April O'Neil",
                 avatar: str = "https://i.pinimg.com/originals/87/67/11/876711e56a0ef942cbb2f15844235f2e.jpg"):
        self.webhook, self.botname, self.avatar = webhook, botname, avatar
        if not webhook.startswith("https://discord.com/api/webhooks/"):
            raise ValueError("Invalid webhook URL")

    def send_message(self, message: str):
        data = json.dumps({"username": self.botname, "avatar_url": self.avatar, "content": message}).encode('utf-8')
        req = Request(self.webhook, data, headers={'Content-Type': 'application/json',
                                                   'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
        try:
            urlopen(req).read()
            return True
        except HTTPError as e:
            print(f"HTTP Error encountered: {e.code} - {e.reason}")
            # Handle HTTPError (like 401, 404, etc.) as needed
        except URLError as e:
            print(f"URL Error encountered: {e.reason}")
            # Handle URLError (like connection errors) as needed
        return False

# Example usage
channel = Discord("https://discord.com/api/webhooks/897529528623194112/Qf3Gfz9u7u8I5rixF9AOsXDas1NoZZLDaFO1Masjdhakshdk1h23123jh")
channel.send_message("What up")

