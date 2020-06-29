import os
import json
import discord as ds
from discord.ext import commands as cmds

class Python(cmds.Cog):

    def __init__(self, client):
        self.client = client

        dirname = os.path.dirname
        rel_path = "./json/cfg.json"
        self.CFG_PATH = os.path.join(dirname(dirname(__file__)), rel_path)

        with open(self.CFG_PATH) as f:
            self.cfg = json.loads(f.read())

        self.ADMIN_ID = self.cfg['Client']['ADMIN ID']

    @cmds.command()
    async def py(self, ctx):
        
        is_admin = ctx.author.roles[-1].id == self.ADMIN_ID
        if is_admin:
            
            await ctx.send(f'```py\n{ctx.message.content[4:]}\n```')
            await ctx.message.delete()

        

def setup(client):
    client.add_cog(Python(client))