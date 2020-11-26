
import os
from os.path import realpath, dirname
import json
import discord
from discord.ext import commands 

# define
CWD = realpath(dirname(__file__))
EXT_PATH = "bot.extensions"
CLIENT_CFG_PATH = os.path.join(CWD, "data/client.json")

class ganja_bot():

    def __init__(self):

        with open(CLIENT_CFG_PATH) as f:
            client_cfg = json.load(f)
        
        self.TOKEN = client_cfg['TOKEN']

        self.client = commands.Bot(**client_cfg['OPTIONS'])

        try:
            self.client.load_extension(f'{EXT_PATH}.commands')
            print(f'commands extension loaded')
        except Exception as e:
            print(e)
        
        for ext in client_cfg['Extensions']:
            try:
                self.client.load_extension(f'{EXT_PATH}.{ext}')
                print(f'{ext} extension loaded')
            except Exception as e:
                print(f'{e}')


    def run(self):
        self.client.run(self.TOKEN)


if __name__ == '__main__':
    EXT_PATH = "extensions"
    client = ganja_bot()
    client.run()