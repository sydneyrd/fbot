from datetime import datetime, timedelta
import tempfile
import subprocess
from io import BytesIO
import os
import asyncio
from functools import partial
import aiohttp
import nextcord as discord
from discord.ext import commands
from my_http import query_uberduck, get_available_voices

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_ROOT = "https://api.uberduck.ai"


class uberduck_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_to_voice_client = dict()
        self.bot.loop.create_task(self.terminate_stale_voice_connections())

    async def terminate_stale_voice_connections(self):
        while True:
            await asyncio.sleep(5)
            for k in list(self.guild_to_voice_client.keys()):
                v = self.guild_to_voice_client[k]
                voice_client, last_used = v
                if datetime.utcnow() - last_used > timedelta(minutes=10):
                    await voice_client.disconnect()
                    self.guild_to_voice_client.pop(k)

    def _context_to_voice_channel(self, ctx):
        return ctx.author.voice.channel if ctx.author.voice else None

    # async def _get_or_create_voice_client(self, ctx):
    #     voice_client = ctx.guild.voice_client
    #     if voice_client:
    #         return voice_client, False

    #     if ctx.author.voice:
    #         voice_channel = ctx.author.voice.channel
    #         voice_client = await voice_channel.connect()
    #         return voice_client, True
    #     else:
    #         raise commands.CommandError("You need to be in a voice channel to use this command.")


    @commands.command()
    async def kick_vc(self, ctx):
        if ctx.guild.id in self.guild_to_voice_client:
            voice_client, _ = self.guild_to_voice_client.pop(ctx.guild.id)
            await voice_client.disconnect()
            await ctx.send("Disconnected from voice channel")
        else:
            await ctx.send("Bot is not connected to a voice channel. Nothing to kick.")

    @commands.command()
    async def speak_vc(self, ctx, voice: str, *, speech:str):  #i want speech to be all of the rest of the words, not just the first
        """Speak a message in voice chat.
        :param voice: The voice to use. See `!voices` for a list of available voices.
        :param speech: The message to speak.
        """
        voice_client, _ = await self._get_or_create_voice_client(ctx)
        if voice_client:
            self.guild_to_voice_client[ctx.guild.id] = (voice_client, datetime.utcnow())
            audio_data = await query_uberduck(speech, voice)
            with tempfile.NamedTemporaryFile(
                suffix=".wav"
            ) as wav_f, tempfile.NamedTemporaryFile(suffix=".opus") as opus_f:
                wav_f.write(audio_data.getvalue())
                wav_f.flush()
                subprocess.check_call(["ffmpeg", "-y", "-i", wav_f.name, opus_f.name])
                source = discord.FFmpegOpusAudio(opus_f.name)
                voice_client.play(source, after=None)

                # Wait for the VoiceClient to connect before playing audio
                while not voice_client.is_connected():
                    await asyncio.sleep(0.1)

                while voice_client.is_playing():
                    await asyncio.sleep(0.5)
                await ctx.send("Sent an Uberduck message in voice chat.")
        else:
            await ctx.send("You're not in a voice channel. Join a voice channel to invite the bot!")
    @staticmethod
    async def play_speech(ctx, voice: str, *, speech:str):  #i want speech to be all of the rest of the words, not just the first
        """Speak a mesage in voice chat.
        :param voice: The voice to use. See `!voices` for a list of available voices.
        :param speech: The message to speak.
        """
        voice_client, _ = await self._get_or_create_voice_client(ctx)
        if voice_client:
            self.guild_to_voice_client[ctx.guild.id] = (voice_client, datetime.utcnow())
            audio_data = await query_uberduck(speech, voice)
            with tempfile.NamedTemporaryFile(
                suffix=".wav"
            ) as wav_f, tempfile.NamedTemporaryFile(suffix=".opus") as opus_f:
                wav_f.write(audio_data.getvalue())
                wav_f.flush()
                subprocess.check_call(["ffmpeg", "-y", "-i", wav_f.name, opus_f.name])
                source = discord.FFmpegOpusAudio(opus_f.name)
                voice_client.play(source, after=None)

                # Wait for the VoiceClient to connect before playing audio
                while not voice_client.is_connected():
                    await asyncio.sleep(0.1)

                while voice_client.is_playing():
                    await asyncio.sleep(0.5)
                await ctx.send("Sent an Uberduck message in voice chat.")
        else:
            await ctx.send("You're not in a voice channel. Join a voice channel to invite the bot!")

    async def _get_or_create_voice_client(self, ctx, channel=None):
        voice_client = ctx.voice_client
        if not voice_client:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        elif voice_client.is_playing() or voice_client.is_paused():
            print("The bot is already playing or paused")
            voice_client.stop()
            voice_client.pause() # Pause the player instead of disconnecting
        return voice_client, channel

    @commands.command()
    async def voice_list(self, ctx):
        await ctx.send("Sending help in private message.")
        await self._send_help(ctx)

    async def _send_help(self, ctx):
        await ctx.author.send(
            "See https://uberduck.ai/quack-help for instructions on using the bot commands. Make sure you enter a voice that exactly matches one of the listed voices."
        )



    


def setup(bot):
    bot.add_cog(uberduck_cog(bot))