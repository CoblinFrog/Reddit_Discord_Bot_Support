import discord, os, json, asyncio, requests, random, string
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CommandInvokeError, has_permissions
from discord.utils import get, find


intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix='=', intents=intents); client.remove_command('help')
YOUR_TOKEN = open("token.txt", "r").readline()


@client.event
async def on_ready():
    print(f'Launched: {client.user.name} // {client.user.id}')


@client.event
async def on_member_join(member):
    with open("json/eco.json", "r+") as f:
        data=json.load(f)
        if not str(member.id) in data:
            data.update({str(member.id) : 100})
            f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()




@client.command()
async def startbet(ctx, *args):
    form_args = list(args); count = ''.join((random.choice(string.ascii_uppercase) for i in range(3)))
    with open('json/eco.json', 'r+') as fs:
        eco_data = json.load(fs); eco_data[str(ctx.author.id)] -= 50 # removes 50$ from their wallet when creating a new bet

    with open("json/bets.json", "r+") as f:
        data=json.load(f)
        data.update({str(count) : {1 : {"players": {}}, 2 : {"players": {}}, "owner" : str(ctx.author.id)}})
        f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()


        ans1 = form_args[len(form_args)-2]; ans2 = form_args[len(form_args)-1]
        q1 = ' '.join(str(enum) for enum in args); question = q1.replace(f' {ans1}', '').replace(f' {ans2}', '')

        await ctx.send(embed=discord.Embed(title=f'Bet #{count}: "{question}"', description=f'1️⃣ **{ans1}**\n2️⃣ **{ans2}**', color=65280))





@client.command()
async def bet(ctx, *args):
    args = list(args)
    with open("json/bets.json", "r+") as f:
        data=json.load(f)

        if not str(ctx.author.id) in data[str(args[0])][str(args[1])]["players"]:
            data[str(args[0])][str(args[1])]["players"].update({str(ctx.author.id) : int(args[2])})
            await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} added a bet of **{args[2]}$**', color=65280))
            f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()
        else:
            data[str(args[0])][str(args[1])]["players"][str(ctx.author.id)] += int(args[2])
            await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} bet is now at **{data[str(args[0])][str(args[1])]["players"][str(ctx.author.id)]}$**', color=65280))
            f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()
        
        with open("json/eco.json", "r+") as eco:
            eco_data = json.load(eco); eco_data[str(ctx.author.id)] -= int(args[2])
            eco.seek(0); json.dump(eco_data, eco, indent=4); eco.truncate(); eco.close()





@client.command()
async def end(ctx, *args):
    args = list(args)
    with open("json/bets.json", "r+") as f:
        data=json.load(f)
        sum = 0; user_count = 0

        if data[str(args[0])]["owner"] == str(ctx.author.id):
            with open("json/eco.json", "r+") as fs:
                data2=json.load(fs)
                if str(args[1]) == "1":
                    for user in data[str(args[0])]["1"]["players"]:
                        user_count += 1
                        sum += data[str(args[0])]["2"]["players"][str(user)] / user_count
                        data2[str(user)] += sum
                        fs.seek(0); json.dump(data2, fs, indent=4); fs.truncate(); fs.close()
                    
                    for user in data[str(args[0])]["2"]["players"]:
                        data2[str(user)] -= sum
                        fs.seek(0); json.dump(data2, fs, indent=4); fs.truncate(); fs.close()
                    

                elif str(args[1]) == "2":
                    for user in data[str(args[0])]["2"]["players"]:
                        user_count += 1
                        sum += data[str(args[0])]["1"]["players"][str(user)] / user_count
                        data2[str(user)] += sum
                        fs.seek(0); json.dump(data2, fs, indent=4); fs.truncate(); fs.close()
                    
                    for user in data[str(args[0])]["1"]["players"]:
                        data2[str(user)] -= sum
                        fs.seek(0); json.dump(data2, fs, indent=4); fs.truncate(); fs.close()


                for line in list(data):
                    if str(args[0]) in line:
                        del data[str(args[0])]
                        f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()

                await ctx.send(embed=discord.Embed(title='Bet Ended', description=f'**Owner: **{ctx.author.mention}\n **Correct Answer: **#{str(args[1])}', color=65280))
        else:
            await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} you are not the owner of this bet', color=65280))





@client.command()
async def wallet(ctx):
    with open("json/eco.json", "r+") as f:
        data=json.load(f)
        await ctx.send(embed=discord.Embed(title='My Wallet', description=f'**User: **{ctx.author.mention}\n**Money: **{data[str(ctx.author.id)]}$', color=65280))




@client.command()
async def pay(ctx, *args):
    with open("json/eco.json", "r+") as f:
        data=json.load(f)
        user_id = str(list(args)[0]).strip("<").strip(">").strip("@").replace('!', '')
        if data[str(ctx.author.id)] -= list(args)[1] > 0:
            data[str(ctx.author.id)] -= list(args)[1]; data[str(user_id)] += list(args)[1]
            f.seek(0); json.dump(data, f, indent=4); f.truncate(); f.close()
            await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} has sent {list(args)[1]} to {list(args)[0]}', color=65280))
        else:
            await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} does not have enough money', color=65280))





client.run(YOUR_TOKEN)
