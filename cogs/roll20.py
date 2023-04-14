import discord
import requests
import random
from discord.ext import commands

class roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll")
    async def roll(self, ctx):
# random number selected between 1 - 20

        random_number = random.randint(1, 20)
        print(random_number)
        embed = discord.Embed(description=random_number, color=discord.Color.blue())
        if random_number==20:
            embed.set_footer(text="(☞ﾟヮﾟ)☞")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(roll(bot))
