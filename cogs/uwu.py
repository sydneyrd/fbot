import uwuify
from discord.ext import commands


class uwu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="uwu")
    async def uwu(self, ctx):
    # Get the message that the command is replying to
        replied_message = ctx.message.reference.resolved
        if replied_message is None:
            await ctx.send("(´･ω･`)?")
            return

        # Get the content of the replied message and uwuify it
        # replied_content = replied_message.content
        # uwuified_content = uwuify.uwu(replied_content)
        # degeneracy = replace_with_emoji(uwuified_content)

        # Send the uwuified message
        # await ctx.send(degeneracy)
        text = replied_message.content

        # Replace some words with emojis
        uwu_text = uwuify.uwu(text)
        final = replace_with_emoji(uwu_text)
        # Send the uwuified text
        await ctx.send(final)


async def setup(bot):
    await bot.add_cog(uwu(bot))



# def replace_with_emoji(text):
#     # Split text into words
#     words = text.split()

#     # Loop over words and replace with emoji if applicable
#     for i, word in enumerate(words):
#         matches = [e for e in emoji.emojize(word).split() if e in emoji.UNICODE_EMOJI['en']]
#         if len(matches) > 0:
#             emoji_name = emoji.demojize(matches[0]).replace(':', '')
#             emoji_char = emoji.emojize(':' + emoji_name + ':')
#             words[i] = emoji_char

#     # Rejoin words into text and return
#     return ' '.join(words)


# def replace_with_emoji(text):
#     # Split text into words
#     words = text.split()

#     # Loop over words and replace with emoji if applicable
#     for i, word in enumerate(words):
#         matches = [e for e in emojis.emojize(word).split() if e in emojis.UNICODE_EMOJI]
#         if len(matches) > 0:
#             emoji_name = emojis.demojize(matches[0]).replace(':', '')
#             emoji_char = emojis.emojize(':' + emoji_name + ':')
#             words[i] = emoji_char

#     # Rejoin words into text and return
#     return ' '.join(words)
