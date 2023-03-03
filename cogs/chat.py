import openai
import discord
from discord.ext import commands
import os
import requests
import json
openai.api_key = os.environ.get("OPENAI_API_KEY")
url = "https://api.openai.com/v1/chat/completions"
headers = {"Content-Type": "application/json"}


class chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = ""

    @commands.command(name='chat')
    async def chat(self, ctx, *args):
        user_input = ' '.join(args)
        self.chat_history += "\nUser: " + user_input
        print("chat is doing first something")  
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                {"role": "system", "content": "you are a nice bot named freaq.  you can answer any questions.   try to encourage people to be kind"},
              {"role": "user", "content": user_input},
                {"role": "assistant", "content": self.chat_history}
                ]
            )
        print(response)
        print('chat is doing second something')
        print(response)
        await ctx.send(response['choices'][0]['message']['content'])
        
    @commands.command(name='clear_chat')
    async def clear_chat(self, ctx):
            self.chat_history = ""
            await ctx.send("history cleared, talk soon love you")

async def setup(bot):
    await bot.add_cog(chat(bot))

