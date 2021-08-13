import discord, os, os.path, json, asyncio, random
from discord.ext import commands
from discord.utils import get, find
from discord.ext.commands import has_permissions
import datetime as datetime
from discord_components import *


class Core(commands.Cog):
    def __init__(self, client):
        self.client = client

    def write(self, file, data, f):
        with open(os.path.dirname(__file__) + f'\\..\\json\\{file}.json', 'w') as x:
            json.dump(data, x, indent=4)
            x.close()


    @commands.command()
    async def add(self, ctx, name: str, image: str):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json', 'r') as f:
            data=json.load(f)
            if not name in data:
                data.update({name: image})
                await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} has added **{name}** to the database', color=65535))
                self.write("data", data, f)
            else:
                await ctx.send(embed=discord.Embed(description=f'**{name}** is already added, use =del to remove it [Mod+]'))


    @commands.command(aliases=['del'])
    @has_permissions(manage_messages=True)
    async def remove(self, ctx, name : str):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json', 'r') as f:
            data=json.load(f)
            for line in data:
                if line == name:
                    del line
                    await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} has removed **{name}** from the database', color=65535))
                    self.write("data", data, f)
        

    @commands.command()
    async def show(self, ctx, name):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json', 'r') as f:
            data=json.load(f)
            if data[name].startswith('http'):
                embed=discord.Embed(title=f'[{name}]', color=65535)
                await embed.set_image(url=data[name])
            else:
                embed=discord.Embed(title=f'[{name}]', description=f'{data[name]}', color=65535)
            await ctx.send(embed=embed)






def setup(client):
    client.add_cog(Core(client))
