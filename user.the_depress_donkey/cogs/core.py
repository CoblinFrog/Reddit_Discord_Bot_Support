import discord, json, os, os.path
from discord.ext import commands

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



# SETTING UP THE COG
# //////////////////
def setup(client):
    client.add_cog(Core(client))
