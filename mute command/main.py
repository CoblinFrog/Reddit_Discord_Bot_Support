import discord, os, json, asyncio
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
@has_permissions(manage_messages=True)
async def mute(ctx, user : discord.Member):
    role = get(ctx.message.guild.roles, name="Muted") # Name of the role you want to add to the person
    await user.add_roles(role)
    await ctx.send(f"Muted {user.mention}")



client.run(YOUR_TOKEN)
