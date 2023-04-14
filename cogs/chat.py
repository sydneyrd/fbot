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
        self.chat_history = [
            {"role": "system", "content": "you are freaq, a chatbot that can talk about anything, is very casual funny, and chill."}
        ]
        self.uberduck = uberduck_cog(bot)
        self.guild_to_voice_client = dict()

    @commands.command(name='freaq')
    async def freaq(self, ctx, *args):
        user_input = ' '.join(args)
        self.chat_history.append({"role": "user", "content": f'{user_input}'}) 
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.chat_history,
            temperature=0.5,
            top_p=0.5,
           
        )
        speech = response.choices[0]['message'].content.strip()
        print(speech)
        self.chat_history.append({"role": "assistant", "content": f'{speech}'})
        voice= 'batman'

        await self.uberduck.play_speech(self, ctx, voice, speech=speech)


    async def _get_or_create_voice_client(self, ctx, channel=None):
        voice_client = ctx.voice_client
        if not voice_client:
            try:
                channel = ctx.author.voice.channel
                voice_client = await channel.connect()
            except Exception: # No channel to join
                print("No channel to join")
                # await ctx.send("You must be in a voice channel to use this command.")
                return None, None,
                
        elif voice_client.is_playing() or voice_client.is_paused():
            print("The bot is already playing or paused")
            voice_client.stop()
            voice_client.pause() # Pause the player instead of disconnecting
        return voice_client, channel

        # await self.uberduck.speak_vc(ctx,  ai_response)

    @commands.command(name='clear_chat')
    async def clear_chat(self, ctx):
        self.chat_history = [
            {"role": "system", "content": "you are freaq, a chatbot that can talk about anything, is very casual funny, and chill."}
        ]
        await ctx.send("Chat history cleared.")

def setup(bot):
    bot.add_cog(freaq(bot))
