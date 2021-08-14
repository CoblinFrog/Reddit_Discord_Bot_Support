import discord, os, os.path, json, asyncio
from discord.ext import commands
from discord.utils import get, find
from discord.ext.commands import has_permissions




class Testing(commands.Cog):
    def __init__(self, client):
        self.client = client

    def write(self, file, data):
        with open(os.path.dirname(__file__) + f'\\..\\json\\{file}.json','w') as f:
            json.dump(data, f, indent=4)


    def cmdCheck(self, cmd, guild):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json','r+') as f:
            data=json.load(f)
            if cmd not in data[str(guild.id)]:
                return True
            return False



    # type =block (command)
    @commands.command()
    @has_permissions(administrator=True)
    async def block(self, ctx, cmd: str):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json','r+') as f:
            data=json.load(f)
            if not str(ctx.message.guild.id) in data:
                data.update({str(ctx.message.guild.id): []})
                data[str(ctx.message.guild.id)].append(cmd)
            else:
                if cmd not in data[str(ctx.message.guild.id)]:
                    data[str(ctx.message.guild.id)].append(cmd)
                    await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} has banned the command **{cmd}**',color=65535))
                else:
                    await ctx.send(embed=discord.Embed(description=f'{ctx.author.mention} **{cmd}** is already banned', color=65535))
            self.write("data", data)




    @commands.command()
    async def test(self, ctx):
        if not self.cmdCheck("=test", ctx.message.guild): # put this with every command you want to check
            await ctx.send("FUCK YOU")
        else:
            await ctx.send("HOLA AMIGO")




    # deletes the message whenver someone types it
    @commands.Cog.listener()
    async def on_message(self, message):
        with open(os.path.dirname(__file__) + f'\\..\\json\\data.json','r+') as f:
            data=json.load(f)
            if message.content in data[str(message.guild.id)]:
                await message.delete()



def setup(client):
    client.add_cog(Testing(client))
