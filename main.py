
import json
import scrapper as sc
import discord as ds
from discord.ext import commands as cmds
from functions import clear_console as ccon

# Json 
with open('cfg.json') as f:
    cfg = json.loads(f.read())

TOKEN = cfg['Bot']['TOKEN']
PREFIX = cfg['Bot']['Command Prefix']

watch_list = cfg['Watch List']


client = cmds.Bot(command_prefix=PREFIX)


@client.event
async def on_ready():
    ccon()
    print('Ganja bot online.')


@client.command()
async def ping(ctx):
    latency = round(client.latency * 1000)
    await ctx.send(f'```fix\nPOW POW {latency}ms```')

@client.command()
async def clear(ctx, amount=1):
    amount += 1
    await ctx.channel.purge(limit=amount)

@client.command()
async def watchlist(ctx, arg1=None, arg2=None):

    await ctx.channel.purge(limit=1)

    if arg1 == 'add':

        cfg['Watch List'].append(str(arg2))
        await ctx.send(f'```{arg2} added to watchlist```')
        with open('cfg.json', 'w') as f:
            json.dump(cfg, f)

    if arg1 == 'remove':

        if arg2 in cfg['Watch List']:

            await ctx.send(f'```removing {arg2} from list```')
            cfg['Watch List'].remove(arg2)
            with open('cfg.json', 'w') as f:
                json.dump(cfg, f)

        else:
            await ctx.send(f'```ticker not found in list```')

    if arg1 == 'quotes':

        wlist = sc.Scrapper.WatchList(cfg['Watch List'])
        await ctx.send(f'```{wlist.data_frame.to_string()}```')

    if arg1 == None:
        await ctx.send('```{}```'.format(cfg['Watch List']))

@client.command()
async def STONKS(ctx):
    await ctx.channel.purge(limit=1)
    wlist = sc.Scrapper.WatchList(cfg['Watch List'])
    await ctx.send(f'```{wlist.data_frame.to_string()}```')

@client.command()
async def stonks(ctx):
    await ctx.channel.purge(limit=1)
    wlist = sc.Scrapper.WatchList(cfg['Watch List'])
    await ctx.send(f'```{wlist.data_frame.to_string()}```')


client.run(TOKEN)
