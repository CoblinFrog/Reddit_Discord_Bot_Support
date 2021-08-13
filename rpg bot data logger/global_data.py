import discord, os, json, asyncio
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandInvokeError
import datetime as datetime
from discord_components import *

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True, voice_states=True)
client = commands.Bot(command_prefix='=', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Collecting RPG Data"))
    print(f" [!] Launched {client.user}")



def write(file, data, f):
     with open(f'json/{file}.json', 'w') as f:
        json.dump(data, f, indent=4); f.close()


def dataUpdate(message, side):
    with open('json/data.json', 'r+') as f:
        data=json.load(f)
        if not str(message.author.id) in data:
            data.update({
                str(message.author.id): {
                    "raids": 0,
                    "defenses": 0,
                    "upgrades": 0
                }})
        else:
            data[str(message.author.id)][f"{side}"] += 1
        write("data", data, f); f.close()



@client.command()
async def check(ctx, *args):
    with open('json/data.json', 'r+') as f:
        data=json.load(f)
        total = data[str(ctx.author.id)]["defenses"] + data[str(ctx.author.id)]["raids"] + data[str(ctx.author.id)]["upgrades"]
        if not args:
            embed=discord.Embed(title=f'{ctx.author.name} points', color=65535)
            embed.add_field(name='Raids', value=f'Amount: **{data[str(ctx.author.id)]["raids"]}**')
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name='Defenses', value=f'Amount: **{data[str(ctx.author.id)]["defenses"]}**')
            embed.add_field(name='Upgrades', value=f'Amount: **{data[str(ctx.author.id)]["upgrades"]}**')
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name='Total', value=f'Amount: **{total}**')
            await ctx.send(embed=embed)

        else:
            user_id = list(args)[0].strip('<').strip('>').strip('@').replace('!')
            embed=discord.Embed(title=f'{list(args)[0]} RPG Data', color=65535)
            embed.add_field(name='Raids', value=f'Amount: **{data[str(user_id)]["raids"]}**')
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name='Defenses', value=f'Amount: **{data[str(user_id)]["defenses"]}**')
            embed.add_field(name='Upgrades', value=f'Amount: **{data[str(user_id)]["upgrades"]}**')
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name='Total', value=f'Amount: **{total}**')
            await ctx.send(embed=embed)



@client.event
async def on_message(message):
    await client.process_commands(message)
    if '=raid' in message.content: # replace "=raid" with whatever command you wanna check for
        await asyncio.sleep(2)
        history =  await message.channel.history(limit=5).flatten() # checks past 5 messages for an embed (change number to higher if the chat is active)
        for msg in history:
            if len(msg.embeds) != 0:
                if "started raid" in msg.embeds[len(msg.embeds)-1].description: # replace "started raid" with whatever words you want to check for
                    dataUpdate(message, "raids")

                elif "started defense" in msg.embeds[len(msg.embeds)-1].description: # replace "started defense" with whatever words you want to check for
                    dataUpdate(message, "defenses")

                elif "upgraded" in msg.embeds[len(msg.embeds)-1].description: # replace "upgraded" with whatever words you want to check for
                    dataUpdate(message, "upgrades")




client.run('YOUR BOT TOKEN')
