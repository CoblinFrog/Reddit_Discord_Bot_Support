import discord, os, json
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
async def track(ctx, *args):
    args = list(args)
    with open("track.json", "r+") as f:
        data = json.load(f)
        if not data[str(date.today().strftime("%d/%m/%Y"))]:
            data.update({str(date.today().strftime("%d/%m/%Y")) : int(args[0])})
            f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()
        else:
            data[str(date.today().strftime("%d/%m/%Y"))] += int(args[0])
            f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()



client.run(YOUR_TOKEN)
