import asyncpraw
import random
import os
import discord
from discord.ext import commands
import random 

class shit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def shit(self, message):
        reddit = await asyncpraw.Reddit(client_id=os.environ.get("REDDIT_ID"),
                     client_secret=os.environ.get("REDDIT_SECRET"),
                     user_agent=os.environ.get("REDDIT_USER_AGENT"))

# Get a subreddit
        subreddit = await reddit.subreddit('shitposting')

        # Get a random submission from the subreddit
        async for random_submission in subreddit.hot(limit=50):
            pass

        # Get all comments for the submission
        await random_submission.comments.replace_more(limit=None)
        comments = random_submission.comments.list()

        # Select a random comment from the list of comments
        random_comment = random.choice(comments)

        # Print the body of the random comment
        print(random_comment.body)

        response = random.comment.body
        await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(shit(bot))
