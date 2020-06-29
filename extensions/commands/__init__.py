
import os
from os.path import realpath, dirname
import json
import discord
import random as rng
from datetime import datetime as dt
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure

class Commands(commands.Cog):

    """ main commands and events from ganja bot """

    def __init__(self, client):
        
        self.client = client
        self.created_at = dt.now()
        
        self.CWD = realpath(dirname(dirname(dirname(__file__))))
        
        self.CLIENT_CFG = os.path.join(self.CWD, "data\\client.json")
        self.OPTIONS_CFG = os.path.join(self.CWD, "data\\options.json")
        self.EXTENSION_PATH = "extensions"

        with open(self.OPTIONS_CFG) as f:
            self.cfg = json.load(f)
        
        with open(self.CLIENT_CFG) as f:
            self.client_cfg = json.load(f)


    @commands.Cog.listener()
    async def on_ready(self):

        """ bot ready message """

        self.ccon()
        print(f'ganja-bot v4.2.0 online.')
        ACTIVITY = discord.Activity(**self.cfg['Activity'])
        await self.client.change_presence(activity=ACTIVITY)


    @commands.command()
    async def ping(self, ctx):

        """ pow """

        self.console_print(ctx)
        await ctx.message.delete()
        latency = round(self.client.latency * 1000)
        await ctx.send(f'```css\nPOW {latency}ms\n```', delete_after=10)


    @commands.command()
    @has_permissions(administrator=True, manage_messages=True, manage_roles=True)
    async def clear(self, ctx, amount=1):

        """
        clears lines
        [amount]: number of lines to be cleared.
        """

        await ctx.message.delete()
        self.console_print(ctx)
        await ctx.channel.purge(limit=amount)


    @commands.command()
    async def roll(self, ctx, sides=6):
        
        """
        rolls a dice
        [sides]: number of sides
        """

        self.console_print(ctx)
        await ctx.message.delete()
        roll = rng.randrange(1, sides + 1)
        await ctx.send(f'```css\nD{sides} roll: {roll:02d}\n```')


    @commands.command()
    async def uptime(self, ctx):

        """ ganja-bot uptime """

        def strfdelta(tdelta, fmt):
            d = {"days": tdelta.days}
            d["hours"], rem = divmod(tdelta.seconds, 3600)
            d["minutes"], d["seconds"] = divmod(rem, 60)
            return fmt.format(**d)

        self.console_print(ctx)
        await ctx.message.delete()

        uptime = dt.now() - self.created_at
        await ctx.send('```diff\n+ Client uptime: {}\n```'\
            .format
            (
                strfdelta
                (
                    uptime,
                    '{days:02d} day(s), {hours:02d} hours, {minutes:02d} minutes')
                )
            )


    @commands.command()
    @has_permissions(administrator=True)
    async def load(self, ctx, extension):

        """ loads extension """

        self.console_print(ctx)
        await ctx.message.delete()

        try:

            self.client.load_extension(f'{self.EXTENSION_PATH}.{extension}')
            await ctx.send(f'```diff\n+ {extension} extension loaded\n```')
            print(f'{extension} extension loaded')

        except Exception as e:
            
            await ctx.send(f'```diff\n- {e}\n```')


    @commands.command()
    @has_permissions(administrator=True)
    async def unload(self, ctx, extension):

        """ unloads extension """

        self.console_print(ctx)
        await ctx.message.delete()

        try:

            self.client.unload_extension(f'{self.EXTENSION_PATH}.{extension}')
            await ctx.send(f'```diff\n- {extension} extension unloaded\n```')
            print(f'{extension} extension unloaded')

        except Exception as e:

            await ctx.send(f'```diff\n- {e}\n```')


    # FUNCTIONS

    def console_print(self, ctx):

        """ prints message info to console """

        now = dt.now().strftime("%m/%d/%y %H:%M:%S")
        print(f'[{now}] {ctx.message.author.name} called {ctx.message.content[1:]}')


    @staticmethod
    def ccon():
        os.system('cls||clear')


def setup(client):
    client.add_cog(Commands(client))