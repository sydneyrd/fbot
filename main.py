import discord
import os
from discord.ext import commands
import asyncio

TOKEN = os.environ.get("DISCORD_KEY")
intents = discord.Intents.all()
# intents.member = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
#looking for the ! before the discord command


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(TOKEN)


asyncio.run(main())


