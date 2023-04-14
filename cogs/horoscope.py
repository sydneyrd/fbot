import nextcord as discord
from discord.ext import commands
import requests
import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")


class horoscope(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def horoscope(self, ctx, *, horoscope, member: discord.Member = None):
        if member is None:
            member = ctx.author
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"write a cool daily horoscope for {horoscope} sign, but make it really uwu-y with lots of emoticons and no punctuation",
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
        )
        description = response.choices[0].text.strip()

        embed_var = discord.Embed(
            title=f"hi {member.display_name}", color=discord.Color.random())
        embed_var.add_field(name="what's up today", value=f'{description}')
        embed_var.set_footer(text='bless')
        await ctx.send(embed=embed_var)


async def setup(bot):
    bot.add_cog(horoscope(bot))
