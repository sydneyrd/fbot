import discord
from discord.ext import commands
import random 

class chainsawman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    # async def on_message(self, message):
    #     if 'chainsaw man' in message.content.lower():
    #         await message.channel.send('chainsaw man sucks')

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'chainsaw man' in message.content.lower():
            response_options = [
                'garbage',
                'trash',
                "lets not fight :(",
                '>:(',
                '😠',
                '😡',
                '😤'
                
            ]
            response = random.choice(response_options)
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(chainsawman(bot))
