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
async def check(ctx):
    messages = await ctx.message.channel.history(limit=200).flatten() # amount of messages you want to look at (200)
    for msg in messages:
        if msg.attachments:
            with open("check.json", "r+") as f:
                data=json.load(f)
                if str(msg.author) not in data:
                    data.update({str(msg.author) : 1})
                    f.seek(0); json.dump(data, f, indent=5); f.truncate()
                else:
                    data[str(msg.author)] += 1

            for user in data:
                await ctx.send(embed=discord.Embed(description=f'{user} has uploaded **{data[str(user)]}** images', color=65535))
            f.close()






client.run(YOUR_TOKEN)
