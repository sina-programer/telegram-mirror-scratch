from urllib.parse import quote, unquote
from urllib.request import urlopen
import json
import time


class Bot:
    base_url = r"https://api.telegram.org/bot{token}/"

    def __init__(self, token):
        if not Bot.check_token(token):
            raise ValueError('Entered token is not valid!')

        self.url = Bot.get_url(token)

    def start(self, delay=2):
        while True:
            self.check_update()
            time.sleep(delay)

    def check_update(self):
        updates = self.get_updates()
        if updates['result']:
            response = None
            update = updates['result'][0]
            update_id = update['update_id']
            message = update['message']
            chat_id = str(message['chat']['id'])
            if 'text' in message:
                response = self.send_message(message['text'], chat_id)
            if response != {}:
                self.offset(update_id+1)

    def send_message(self, text, chat_id, encoding='utf-8'):
        text = quote(text.encode(encoding))
        response = Bot.fetch_url(self.url + f'sendMessage?chat_id={chat_id}&text={text}')
        if response['ok']:
            return response
        return {}

    def offset(self, update_id):
        urlopen(self.url + f'getUpdates?offset={update_id}')

    def get_updates(self):
        return Bot.fetch_url(self.url + 'getUpdates')

    @staticmethod
    def check_token(token):
        result = Bot.fetch_url(Bot.base_url.format(token=token) + 'getme')
        return result['ok'] and result['result']['is_bot']

    @staticmethod
    def fetch_url(url, encoding='utf-8'):
        return json.loads(urlopen(url).read().decode(encoding))

    @classmethod
    def get_url(cls, token):
        return cls.base_url.format(token=token)


TOKEN = 'your intended token'


if __name__ == "__main__":
    bot = Bot(TOKEN)
    bot.start()
