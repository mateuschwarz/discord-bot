# === ganja-bot v4.2.0 ===

import json
import scrapper as sc
import discord as ds
from discord.ext import commands as cmds
from functions import clear_console as ccon


# configurations

with open('cfg.json') as f:
    cfg = json.loads(f.read())

TOKEN = cfg['Bot']['TOKEN']
PREFIX = cfg['Bot']['Command Prefix']
WLIST = cfg['Watch List']
ADMIN_ID = 424253447403995148

client = cmds.Bot(command_prefix=PREFIX)


# commands and events

@client.event
async def on_ready():

    """ bot ready message """

    ccon()
    print('Ganja bot online.')


@client.command()
async def ping(ctx):

    """ command: !ping """

    await ctx.channel.purge(limit=1)
    latency = round(client.latency * 1000)
    await ctx.send(f'```fix\nPOW {latency}ms```')


@client.command()
async def clear(ctx, amount=1):

    """
    clears set amount of lines in channel

    command: !clear <amount>
    :amount: number of lines to clear

    """

    if ctx.author.roles[-1].id == ADMIN_ID:
        amount += 1
        await ctx.channel.purge(limit=amount)



@client.command()
async def watchlist(ctx, cmd=None, args=None):

    """
    command: !watchlist <cmd> <args>

    :cmd: command
    :args: arguments if necessary

    """

    role = ctx.author.roles
    is_admin = role[-1].id == ADMIN_ID
    await ctx.channel.purge(limit=1)

    # !watchlist add {TICKER}
    if cmd == 'add':

        if is_admin:

            WLIST.append(str(args))
            await ctx.send(f'```{args} added to watchlist```')
            with open('cfg.json', 'w') as f:
                json.dump(cfg, f)

        else:
            await ctx.send(f'```admin only command```')


    # !watchlist remove {TICKER}
    if cmd == 'remove':

        if is_admin:
            
            try:

                WLIST.remove(args)
                await ctx.send(f'```{args} removed from watchlist```')
                with open('cfg.json', 'w') as f:
                    json.dump(cfg, f)

            except:
                await ctx.send(f'```{args} ticker not found in list```')

        else:
            await ctx.send(f'```admin only command```')


    # !watchlist quotes
    if cmd == 'quotes':

        wlist = sc.Scrapper.WatchList(WLIST)
        await ctx.send(f'```Quotes:\n{wlist.data_frame.to_string()}```')

    if cmd == None:
        await ctx.send('```Watchlist:\n{}```'.format(WLIST))


@client.command()
async def STONKS(ctx):

    """ !STONKS """

    await ctx.channel.purge(limit=1)
    wlist = sc.Scrapper.WatchList(cfg['Watch List'])
    await ctx.send(f'```{wlist.data_frame.to_string()}```')


@client.command()
async def stonks(ctx):

    """ !stonks """

    await ctx.channel.purge(limit=1)
    wlist = sc.Scrapper.WatchList(cfg['Watch List'])
    await ctx.send(f'```{wlist.data_frame.to_string()}```')


client.run(TOKEN)
