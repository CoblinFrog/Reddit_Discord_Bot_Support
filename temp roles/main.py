import discord, os, json, asyncio
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandInvokeError, has_permissions
import datetime as datetime
from datetime import date
from discord.utils import get, find


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='=', intents=intents); client.remove_command('help')
YOUR_TOKEN = open("token.txt", "r").readline()


@client.event
async def on_ready():
    print(f'Launched: {client.user.name} // {client.user.id}')



@client.command()
async def temp(ctx, *args):
    role = get(ctx.message.guild.roles, name = "Role") # change this to the name of the role you want
    for user in ctx.message.guild.members:
        user.add_roles(role)
    await ctx.send("Successfully added {role} to everyone")

    asyncio.sleep(10)  # how long you want it to be until the role is removed (seconds)

    for user in ctx.message.guild.members:
        user.remove_roles(role)
    await ctx.send("Successfully removed {role} from everyone")



client.run(YOUR_TOKEN)
