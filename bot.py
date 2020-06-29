
import json
import discord as ds
import random as rng
from datetime import datetime as dt
from discord.ext import commands as cmds
from scrapper.scrapper import Scrapper as sc

class GanjaBot(cmds.Cog):


    def __init__(self, client):
        self.client = client

        self.CFG_PATH = "./json/cfg.json"

        with open(self.CFG_PATH) as f:
            self.cfg = json.loads(f.read())

        self.ADMIN_ID = self.cfg['Client']['ADMIN ID']
        self.WLIST = self.cfg['Watch List']
        self.ACTIVITY = ds.Game(name=self.cfg['Activity']['name'])

        self.Scrapper = sc    


    @cmds.command()
    async def ping(self, ctx):

        """ pow """

        self.console_print(ctx)
        await ctx.message.delete()
        latency = round(self.client.latency * 1000)
        await ctx.send(f'```css\nPOW {latency}ms\n```', delete_after=10)


    @cmds.command()
    async def clear(self, ctx, amount=1):

        """
        clears lines
        [amount]: number of lines to be cleared.
        """

        self.console_print(ctx)
        if ctx.author.roles[-1].id == self.ADMIN_ID:
            amount += 1
            await ctx.channel.purge(limit=amount)



    @cmds.command()
    async def watchlist(self, ctx, cmd=None, args=None):

        """
        stock watchlist 
        [cmd]:
        add: adds [args] to watchlist
        remove: remove [args] from watchlist
        quotes: returns todays quotes
        None: returns watchlist tickers
        """

        self.console_print(ctx)
        role = ctx.author.roles
        is_admin = role[-1].id == self.ADMIN_ID
        await ctx.message.delete()

        # !watchlist add {TICKER}
        if cmd == 'add':

            if is_admin:

                self.WLIST.append(str(args))
                await ctx.send(f'```diff\n+ {args} added to watchlist\n```')
                with open(self.CFG_PATH, 'w') as f:
                    json.dump(self.cfg, f)

            else:
                await ctx.send(f'```css\nadmin only command\n```')


        # !watchlist remove {TICKER}
        if cmd == 'remove':

            if is_admin:
                
                try:

                    self.WLIST.remove(args)
                    await ctx.send(f'```diff\n- {args} removed from watchlist\n```')
                    with open(self.CFG_PATH, 'w') as f:
                        json.dump(self.cfg, f)

                except:
                    await ctx.send(f'```css\n{args} ticker not found in list\n```')

            else:
                await ctx.send(f'```css\nadmin only command\n```')


        # !watchlist quotes
        if cmd == 'quotes':

            wlist = self.Scrapper.WatchList(self.WLIST)
            await ctx.send(f'```diff\n+ quotes:\n{wlist.data_frame.to_string()}\n```')

        # no command
        if cmd == None:
            await ctx.send(f'```diff\n+ watchlist:\n{self.WLIST}```')



    @cmds.command()
    async def stonks(self, ctx):

        """ returns quotes from watchlist """

        self.console_print(ctx)
        await ctx.message.delete()
        wlist = self.Scrapper.WatchList(self.cfg['Watch List'])
        await ctx.send(f'```{wlist.data_frame.to_string()}```')


    @cmds.command()
    async def roll(self, ctx, sides=6):
        
        """
        rolls a dice
        [sides]: number of sides
        """

        self.console_print(ctx)
        await ctx.message.delete()
        roll = rng.randrange(1, sides + 1)
        await ctx.send(f'```css\nD{sides} roll: {roll:02d}\n```')


    @cmds.command()
    async def uptime(self, ctx):

        def strfdelta(tdelta, fmt):
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            return fmt.format(**d)

        self.console_print(ctx)
        await ctx.message.delete()

        uptime = dt.now() - self.client.user.created_at
        await ctx.send('```diff\n+ Client uptime: {}\n```'\
            .format(strfdelta(uptime, '{days:02d} day(s) {hours}:{minutes}')))


    def console_print(self, ctx):
        now = dt.now().strftime("%m/%d/%y %H:%M:%S")
        print(f'[{now}] {ctx.message.author.name} called {ctx.message.content[1:]}')


def setup(client):
    client.add_cog(GanjaBot(client))