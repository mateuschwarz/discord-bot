# === ganja-bot v4.2.0 ===

import os
import json
import discord
from discord.ext import commands


# reading client file

CLIENT_CFG_PATH = "./json/client.json"
COGS_PATH = "cogs"

with open(CLIENT_CFG_PATH) as f:
    client_cfg = json.load(f)


# setting up client

client = commands.Bot(**client_cfg['OPTIONS'])

client.load_extension(f'bot')

for cogs in client_cfg['Cogs']:
    try:
        client.load_extension(f'{COGS_PATH}.{cogs}')
        print(f'{cogs} extension loaded')
    except Exception as e:
        print(f'{e}')

client.run(client_cfg['TOKEN'])
