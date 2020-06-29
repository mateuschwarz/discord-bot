
import os
import json
from datetime import datetime as dt

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from scrapper.scrapper import Scrapper as sc


class Stonks(commands.Cog):

    def __init__(self, client):

        self.client = client

        main_dir = os.path.dirname(os.path.dirname(__file__))
        rel_path = "./json/stonks.json"
        self.STONKS_PATH = os.path.join(main_dir, rel_path)

        with open(self.STONKS_PATH) as f:
            self.cfg = json.load(f)

        self.WLIST = self.cfg['Watch List']
        self.Scrapper = sc

    @commands.command()
    @has_permissions(administrator=True)
    async def watchlist(self, ctx, cmd=None, args=None):

        """
        watchlist commands and configurations 
        [cmd]:
        add: adds [args] to watchlist
        remove: remove [args] from watchlist
        quotes: returns todays quotes
        None: returns watchlist tickers
        """

        self.console_print(ctx)
        await ctx.message.delete()

        # !watchlist add {TICKER}
        if cmd == 'add':

            self.WLIST.append(args)
            await ctx.send(f'```diff\n+ {args} added to watchlist\n```')
            with open(self.STONKS_PATH, 'w') as f:
                json.dump(self.cfg, f, indent=4)


        # !watchlist remove {TICKER}
        if cmd == 'remove':

            try:

                self.WLIST.remove(args)
                await ctx.send(f'```diff\n- {args} removed from watchlist\n```')
                with open(self.STONKS_PATH, 'w') as f:
                    json.dump(self.cfg, f, indent=4)

            except:
                await ctx.send(f'```diff\n- {args} ticker not found in list\n```')


        # !watchlist quotes
        if cmd == 'quotes':

            wlist = self.Scrapper.WatchList(self.WLIST)
            await ctx.send(f'```diff\n+ quotes:\n{wlist.data_frame.to_string()}\n```')

        # no command
        if cmd == None:
            await ctx.send(f'```diff\n+ watchlist:\n{self.WLIST}```')



    @commands.command()
    async def stonks(self, ctx):

        """ returns quotes from watchlist """

        self.console_print(ctx)
        await ctx.message.delete()
        wlist = self.Scrapper.WatchList(self.cfg['Watch List'])
        await ctx.send(f'```diff\n+ watchlist quotes:\n{wlist.data_frame.to_string()}\n```')

    
    # FUNCTIONS

    def console_print(self, ctx):

        """ prints message info to console """

        now = dt.now().strftime("%m/%d/%y %H:%M:%S")
        print(f'[{now}] {ctx.message.author.name} called {ctx.message.content[1:]}')


    @staticmethod
    def ccon():
        os.system('cls||clear')


def setup(client):
    client.add_cog(Stonks(client))