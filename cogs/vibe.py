import discord
import requests
import random
from discord.ext import commands

class vibe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vibe")
    async def vibe(self, ctx):
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            quote = data["content"]
            embed = discord.Embed(description=quote, color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send("sorry charlie :(")

async def setup(bot):
    await bot.add_cog(vibe(bot))
