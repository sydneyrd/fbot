import nextcord as discord
from discord.ext import commands
import requests

class horoscope(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def horoscope(self, ctx, *, horoscope, member:discord.Member = None):
        if member is None:
            member = ctx.author
        params = (
        ('sign', f"{horoscope}"),
        ('day', 'today'),)
        r = requests.post('https://aztro.sameerkumar.website/', params=params)
        res = r.json()
        mood = res['mood']
        description = res['description']
        date_range = res['date_range']

        embed_var = discord.Embed(title=f"hi {member.display_name}", description=f"{date_range}", color=discord.Color.random())
        embed_var.add_field(name='how u do', value=f'{mood}', inline=True)
        embed_var.add_field(name="what's up today", value=f'{description}')
        embed_var.set_footer(text='bless')
        await ctx.send(embed=embed_var)

async def setup(bot):
    bot.add_cog(horoscope(bot))