#! /usr/bin/env python3

from telegram import Bot
from config import TELE_TOKEN

bot = Bot(token=TELE_TOKEN)

while True:
    print('Fetching get_updates()...')
    try:
        print(bot.get_updates()[0].message.chat_id)
    except IndexError:
        print('IndexError: likely no updates received')
    input()
