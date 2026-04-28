import discord
import feedparser
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
RSS_URL = "https://seauxsims.tumblr.com/rss"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_post = None

async def check_rss():
    global last_post
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            latest = feed.entries[0].link
            if latest != last_post:
                last_post = latest
                if channel:
                    await channel.send(f"New Tumblr post 💜\n{latest}")
        await asyncio.sleep(600)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.loop.create_task(check_rss())
client.run(TOKEN)
