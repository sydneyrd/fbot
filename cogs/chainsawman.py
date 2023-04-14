import nextcord as discord
from discord.ext import commands
import random 

class chainsawman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if 'chainsaw man' in message.content.lower():
            response_options = [
                'garbage',
                'trash',
                "lets not fight :(",
                'shit',
                '>:(',
                '😠',
                '😡',
                '😤'
                
            ]
            response = random.choice(response_options)
            await message.channel.send(response)

async def setup(bot):
    bot.add_cog(chainsawman(bot))
