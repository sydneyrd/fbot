import nextcord as discord
import requests
import random
from discord.ext import commands

class vibe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vibe")
    async def vibe(self, ctx):
        try:
            response = requests.get("https://api.quotable.io/random")
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            await ctx.send(f"HTTP error occurred: {err}")
        except Exception as err:
            await ctx.send(f"Other error occurred: {err}")
        else:
            data = response.json()
            quote = data["content"]
            embed = discord.Embed(description=quote, color=discord.Color.blue())
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(vibe(bot))
