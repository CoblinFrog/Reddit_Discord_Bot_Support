import discord, os, json, asyncio, requests
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandInvokeError, has_permissions
from discord.utils import get, find


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='=', intents=intents); client.remove_command('help')
YOUR_TOKEN = open("token.txt", "r").readline()


@client.event
async def on_ready():
    print(f'Launched: {client.user.name} // {client.user.id}')





@client.command()
async def insult(ctx, user : discord.Member):
    r = requests.get('https://insult.mattbas.org/api/en/insult.txt')
    await ctx.send(embed=discord.Embed(description=f'{user.mention} **{r.text}**', color=16711680))










client.run(YOUR_TOKEN)
