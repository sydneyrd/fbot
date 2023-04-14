import nextcord as discord
from discord.ext import commands
import datetime
from typing import Union

class zodiac(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

   
    @commands.command()
    async def zodiac(self, ctx, date: str):
        date_components = date.split("/")
        month, day = map(int, date_components[:2])
        sign = self.get_zodiac_sign(month, day)
        await ctx.send(f"Your zodiac sign is {sign}.")


    def get_zodiac_sign(self, month, day):
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return "Aries"
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return "Taurus"
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return "Gemini"
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return "Cancer"
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return "Leo"
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return "Virgo"
        elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
            return "Libra"
        elif (month == 10 and day >= 24) or (month == 11 and day <= 21):
            return "Scorpio"
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return "Sagittarius"
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return "Capricorn"
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return "Aquarius"
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return "Pisces"
            

def parse_date(date_str: str) -> Union[None, tuple]:
        date_format_1 = "%m/%d/%y"
        date_format_2 = "%m/%d/%Y"
        try:
            return datetime.datetime.strptime(date_str, date_format_1).date().month, datetime.datetime.strptime(date_str, date_format_1).date().day
        except ValueError:
            try:
                return datetime.datetime.strptime(date_str, date_format_2).date().month, datetime.datetime.strptime(date_str, date_format_2).date().day
            except ValueError:
                return None

async def setup(bot):
    bot.add_cog(zodiac(bot))