
import os
from os.path import realpath, dirname
import json

import discord
from discord.ext import commands 

# Define
CLIENT_CFG_PATH = "data\\client.json"
EXT_PATH = "extensions"


class ganja_bot():

    def __init__(self):

        cwd = realpath(dirname(__file__))
        cfg_path = os.path.join(cwd, CLIENT_CFG_PATH)

        with open(cfg_path) as f:
            client_cfg = json.load(f)
        
        self.TOKEN = client_cfg['TOKEN']

        self.client = commands.Bot(**client_cfg['OPTIONS'])

        self.client.load_extension(f'extensions.commands')
        
        for ext in client_cfg['Extensions']:
            try:
                self.client.load_extension(f'{EXT_PATH}.{ext}')
                print(f'{ext} extension loaded')
            except Exception as e:
                print(f'{e}')


    def run(self):
        self.client.run(self.TOKEN)


if __name__ == '__main__':
    client = ganja_bot()
    client.run()