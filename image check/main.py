import discord
from discord.ext import commands


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='=', intents=intents); client.remove_command('help')
YOUR_TOKEN = open("token.txt", "r").readline()


@client.event
async def on_ready():
    print(f'Launched: {client.user.name} // {client.user.id}')


    
@client.command()
async def check(ctx, user : discord.Member):
    count = 0
    messages = await ctx.message.channel.history().flatten()
    for msg in messages:
        if msg.author == user and msg.attachments:
            count += 1
    await ctx.send(embed=discord.Embed(description=f'{user} has uploaded **{count}** images', color=65535))



    
client.run(YOUR_TOKEN)
