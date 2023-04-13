from datetime import datetime, timedelta
import tempfile
import subprocess
from io import BytesIO
import asyncio
import aiohttp
import nextcord as discord
from discord.ext import commands
from ..http import query_uberduck

API_KEY = "replace-me"
API_SECRET = "replace-me"
API_ROOT = "https://api.uberduck.ai"


class UberduckCog(commands.Cog):
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

    async def _get_or_create_voice_client(self, ctx: commands.Context):
        joined = False
        if ctx.guild.id in self.guild_to_voice_client:
            voice_client, _ = self.guild_to_voice_client[ctx.guild.id]
        else:
            voice_channel = self._context_to_voice_channel(ctx)
            if voice_channel is None:
                voice_client = None
            else:
                voice_client = await voice_channel.connect()
                joined = True
        return (voice_client, joined)

    @commands.command()
    async def join_vc(self, ctx):
        voice_client, joined = await self._get_or_create_voice_client(ctx)
        if voice_client is None:
            await ctx.send("You're not in a voice channel. Join a voice channel to invite the bot!")
        elif ctx.author.voice and voice_client.channel.id != ctx.author.voice.channel.id:
            old_channel_name = voice_client.channel.name
            await voice_client.disconnect()
            voice_client = await ctx.author.voice.channel.connect()
            new_channel_name = voice_client.channel.name
            self.guild_to_voice_client[ctx.guild.id] = (
                voice_client, datetime.utcnow())
            await ctx.send(f"Switched from #{old_channel_name} to #{new_channel_name}!")
        else:
            await ctx.send("Connected to voice channel!")
            self.guild_to_voice_client[ctx.guild.id] = (
                voice_client, datetime.utcnow())

    @commands.command()
    async def kick_vc(self, ctx):
        if ctx.guild.id in self.guild_to_voice_client:
            voice_client, _ = self.guild_to_voice_client.pop(ctx.guild.id)
            await voice_client.disconnect()
            await ctx.send("Disconnected from voice channel")
        else:
            await ctx.send("Bot is not connected to a voice channel. Nothing to kick.")

    @commands.command()
    async def speak_vc(self, ctx, voice: str, speech: str):
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
                source = nextcord.FFmpegOpusAudio(opus_f.name)
                voice_client.play(source, after=None)
                while voice_client.is_playing():
                    await asyncio.sleep(0.5)
                await ctx.send("Sent an Uberduck message in voice chat.")
        else:
            await ctx.send("You're not in a voice channel. Join a voice channel to invite the bot!")

    @commands.command()
    async def quack_help(self, ctx):
        await ctx.send("Sending help in private message.")
        await self._send_help(ctx)

    async def _send_help(self, ctx):
        await ctx.author.send(
            "See https://uberduck.ai/quack-help for instructions on using the bot commands. Make sure you enter a voice that exactly matches one of the listed voices."
        )

def setup(bot):
    bot.add_cog(UberduckCog(bot))