import discord, json, os, os.path
from discord.ext import commands
from discord.ext.commands import has_permissions

class Core(commands.Cog):
    def __init__(self, client):
        self.client = client

    # FUNCTION USED TO WRITE DATA TO THE JSON FILE
    # ////////////////////////////////////////////
    def write(self, file, data):
        with open(os.path.dirname(__file__) + f"\\..\\json\\{file}.json", "w") as f:
            json.dump(data, f, indent=4)



    # ON MEMBER JOIN, ADD THEM TO THE JSON FILE 
    # /////////////////////////////////////////
    @commands.Cogs.listener
    async def on_member_join(self, member):
        with open(os.path.dirname(__file__) + f"\\..\\json\\data.json", "r+") as f:
            data=json.load(f)
            data["users"].append(member)
            self.write("data", data)
    


    # ON MEMBER LEAVE, REMOVE THEM FROM THE JSON FILE
    # ///////////////////////////////////////////////
    @commands.Cogs.listener
    async def on_member_leave(self, member):
        with open(os.path.dirname(__file__) + f"\\..\\json\\data.json", "r+") as f:
            data=json.load(f)
            data["users"].remove(member)
            self.write("data", data)
        
        await member.send("Message you want to send them when they leave the server")



    # RESET THE USERS LIST AND ADD EVERYONE IN THE SERVER TO IT (=members COMMAND)
    # /////////////////////////////////////////////////////////
    @commands.command()
    @has_permissions(administrator=True)
    async def members(self, ctx):
        with open(os.path.dirname(__file__) + f"\\..\\json\\data.json", "r+") as f:
            data=json.load(f)
            data["users"] = []
            for user in ctx.guild.members:
                data["users"].append(user)
            self.write("data", data)
        await ctx.send(embed=discord.Embed(title='Member', description=f'{data["users"]}', color=65535))




# SETTING UP THE COG
# //////////////////
def setup(client):
    client.add_cog(Core(client))
