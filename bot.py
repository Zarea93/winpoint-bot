import discord
import requests
import asyncio
import os

# ------------------------------
# Čitanje env varijabli
# ------------------------------
TOKEN = os.getenv("TOKEN")
CHANNEL_ID_ENV = os.getenv("CHANNEL_ID")

# Provera da li su setovane
if not TOKEN:
    raise RuntimeError("TOKEN nije postavljen u Environment Variables!")

if not CHANNEL_ID_ENV:
    raise RuntimeError("CHANNEL_ID nije postavljen u Environment Variables!")

try:
    CHANNEL_ID = int(CHANNEL_ID_ENV)
except ValueError:
    raise RuntimeError("CHANNEL_ID mora biti BROJ!")

# ------------------------------
# Konfiguracija bota
# ------------------------------
URL = "https://winpoint.gg"

intents = discord.Intents.default()
intents.message_content = True  # neophodno za slanje poruka

client = discord.Client(intents=intents)

old_page = ""  # čuvanje stare stranice

# ------------------------------
# Funkcija za dobavljanje stranice
# ------------------------------
def get_page():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=headers, timeout=10)
        return r.text
    except Exception as e:
        print("HTTP GREŠKA:", e)
        return None

# ------------------------------
# Kada bot bude spreman
# ------------------------------
@client.event
async def on_ready():
    print(f"Bot je online kao {client.user}")
    # Startuje check loop
    asyncio.create_task(check_loop())

# ------------------------------
# Glavni loop za proveru stranice
# ------------------------------
async def check_loop():
    global old_page
    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        raise RuntimeError(f"Ne mogu da nadjem kanal sa ID {CHANNEL_ID}. Proveri permissions i ID!")

    print(f"Bot će slati poruke u kanal: {channel.name} ({CHANNEL_ID})")

    while True:
        page = get_page()
        if page is not None:
            if old_page and page != old_page:
                try:
                    await channel.send("@everyone 🆕 New matches are added on winpoint.gg")
                except Exception as e:
                    print("GREŠKA prilikom slanja poruke:", e)
            old_page = page
        # čekaj 60 sekundi pre sledeće provere
        await asyncio.sleep(60)

# ------------------------------
# Pokretanje bota
# ------------------------------
client.run(TOKEN)
