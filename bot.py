import discord
import requests
import asyncio
import os

# Čitanje tokena i channel ID iz Environment Variables
TOKEN = os.getenv("TOKEN")
channel_id_env = os.getenv("CHANNEL_ID")

if not TOKEN:
    raise ValueError("TOKEN nije postavljen u Environment Variables!")
if not channel_id_env:
    raise ValueError("CHANNEL_ID nije postavljen u Environment Variables!")

try:
    CHANNEL_ID = int(channel_id_env)
except ValueError:
    raise ValueError("CHANNEL_ID mora biti broj!")

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

    # Čekanje dok bot ne učita kanal
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Ne mogu da pronađem kanal sa ID {CHANNEL_ID}. Proveri permissions i ID.")
        return

    while True:
        page = get_page()

        if old_page and page != old_page:
            await channel.send("@everyone 🆕 New matches are added on winpoint.gg")

        old_page = page
        await asyncio.sleep(60)

# Pokretanje bota
client.run(TOKEN)
