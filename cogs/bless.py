# import discord
# import requests
# from discord.ext import commands

# class bless(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.command(name="bless")
#     async def bless(self, ctx):
#         response = requests.get("https://complimentr.com/api")
#         if response.status_code == 200:
#             data = response.json()
#             compliment = data["compliment"]
#             embed = discord.Embed(description=compliment, color=discord.Color.red())
#             await ctx.send(embed=embed)
#         else:
#             await ctx.send("sorry charlie :(")

# async def setup(bot):
#     await bot.add_cog(bless(bot))
import nextcord as discord
import requests
from discord.ext import commands

class bless(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bless")
    async def bless(self, ctx, user: discord.User):
        response = requests.get("https://complimentr.com/api")
        if response.status_code == 200:
            data = response.json()
            compliment = data["compliment"]
            embed = discord.Embed(description=compliment, color=discord.Color.red())
            await user.send(embed=embed)
        else:
            await ctx.send("sorry charlie :(")

async def setup(bot):
    bot.add_cog(bless(bot))
