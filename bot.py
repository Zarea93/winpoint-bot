import discord
import requests
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

URL = "https://winpoint.gg"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

old_page = ""

def get_page():
    headers = {"User-Agent": "Mozilla/5.0"}
    return requests.get(URL, headers=headers).text

@client.event
async def on_ready():
    print("Bot radi")
    client.loop.create_task(check())

async def check():
    global old_page
    channel = client.get_channel(CHANNEL_ID)

    while True:
        page = get_page()

        if old_page and page != old_page:
            await channel.send("@everyone 🆕 New matches are added on winpoint.gg")

        old_page = page
        await asyncio.sleep(60)

client.run(TOKEN)
