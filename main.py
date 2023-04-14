import nextcord as discord
import os
from discord.ext import commands
import asyncio
import logging


logger = logging.getLogger('nextcord')

TOKEN = os.getenv("BOT_TOKEN")


intents = discord.Intents.all()
# intents.member = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
#looking for the ! before the discord command


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            logger.info(f'Loading cog: {filename}')
            bot.load_extension(f'cogs.{filename[:-3]}')
            logger.info(f'Loaded cog: {filename}')

# async def main():
#     await load()
#     await bot.start(f"{TOKEN}")

async def start_bot():
    await load()

    print('hellllloooooooo')
    await bot.start(TOKEN)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())




# asyncio.run(main())


