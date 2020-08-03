import os
import praw
import discord
from discord.ext import commands
import logging
from keep_alive import keep_alive

# LOGGING START
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# LOGGING END

# API initialization

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"))

bot = commands.Bot(
    command_prefix='!', 
    activity=discord.Activity(name='!qtgirls', type=discord.ActivityType.listening)
)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def qtgirls(ctx, *args):
    if str(ctx.message.channel) != "jins-pleasure-bot":
        return
    submission = reddit.subreddit("AnimeGirls+CuteAnimeGirls+awwnime").random()
    try:
        while submission.over_18 or submission.is_self:  # stops NSFW/text posts from showing up
            submission = reddit.subreddit(
                "AnimeGirls+CuteAnimeGirls+awwnime").random()
    except Exception as e:
        ctx.send(e)
        print(e)
        pass
    embed = discord.Embed(
        title=submission.title,
        url=f'https://reddit.com{submission.permalink}',
    )
    embed.set_image(url=submission.url)
    embed.set_author(
        name=submission.author.name,
        url=f"https://reddit.com/u/{submission.author.name}",
        icon_url=submission.author.icon_img)
    embed.set_footer(
        text=f"From {submission.subreddit}")
    await ctx.send(embed=embed)


keep_alive()
bot.run(os.environ.get('DISCORD_BOT_SECRET'))