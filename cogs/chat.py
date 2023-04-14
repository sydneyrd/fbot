import nextcord as discord
from discord.ext import commands
import os
import requests
import json
import openai
import tempfile
import subprocess
from datetime import datetime
from io import BytesIO
from .uberduck_cog import query_uberduck, uberduck_cog

openai.api_key = os.environ.get("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"
headers = {"Content-Type": "application/json"}

class freaq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = ""
        # self.uberduck = uberduck_cog(bot)

    @commands.command(name='freaq')
    async def freaq(self, ctx, *args):
        user_input = ' '.join(args)
        self.chat_history += "\nUser: " + user_input
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{self.chat_history}\nUser: {user_input}\nAI:",
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
        speech = response.choices[0].text.strip()
        print(speech)
        self.chat_history += "\nAI: " + speech
        voice= 'batman' 

        await uberduck_cog.play_speech(ctx, voice, speech)




        # await self.uberduck.speak_vc(ctx,  ai_response)

    @commands.command(name='clear_chat')
    async def clear_chat(self, ctx):
        self.chat_history = ""
        await ctx.send("Chat history cleared.")

def setup(bot):
    bot.add_cog(freaq(bot))
