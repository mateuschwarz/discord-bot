# === ganja-bot v4.2.0 ===

import os
import json
import discord as ds
from discord.ext import commands as cmds


# configurations

ccon = lambda : os.system('cls||clear')

CFG_PATH = "./json/cfg.json"

with open(CFG_PATH) as f:
    cfg = json.loads(f.read())

COGS_PATH = "cogs"
ADMIN_ID = cfg['Client']['ADMIN ID']

client = cmds.Bot(**cfg['Client']['Options'])


# base events and commands

@client.event
async def on_ready():

    """ bot ready message """

    ccon()
    now = client.user.created_at.strftime("%m/%d/%y %H:%M:%S")
    print(f'ganja-bot v4.2.0 online.')
    print(f'created at: {now}')
    print()
    ACTIVITY = ds.Activity(**cfg['Activity'])
    await client.change_presence(activity=ACTIVITY)


@client.command()
async def load(ctx, extension):

    if ctx.author.roles[-1].id == ADMIN_ID:
        await ctx.message.delete()
        await ctx.send(f'```diff\n+ Loading {extension} extension\n```')
        client.load_extension(f'{COGS_PATH}.{extension}')


@client.command()
async def unload(ctx, extension):

    if ctx.author.roles[-1].id == ADMIN_ID:
        await ctx.message.delete()
        await ctx.send(f'```diff\n- Unloading {extension} extension\n```')
        client.unload_extension(f'{COGS_PATH}.{extension}')


# loading extensions

client.load_extension(f'bot')


# client start

client.run(cfg['Client']['TOKEN'])
