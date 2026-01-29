import discord
import aiohttp
import asyncio
import os

# ------------------------------
# Konfiguracija
# ------------------------------
TOKEN = os.getenv("TOKEN")
CHANNEL_ID_ENV = os.getenv("CHANNEL_ID")
URL = "https://winpoint.gg"

if not TOKEN or not CHANNEL_ID_ENV:
    raise RuntimeError("TOKEN ili CHANNEL_ID nisu postavljeni u Environment Variables!")

try:
    CHANNEL_ID = int(CHANNEL_ID_ENV)
except ValueError:
    raise RuntimeError("CHANNEL_ID mora biti broj!")

# Intenti za bota
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# Koristimo hash ili dužinu teksta za poređenje da ne bismo čuvali preogromne stringove
old_content_hash = None

# ------------------------------
# Funkcija za proveru stranice (Asinhrona)
# ------------------------------
async def fetch_page():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL, headers=headers, timeout=15) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Sajt vratio status: {response.status}")
                    return None
    except Exception as e:
        print(f"Greška prilikom konekcije: {e}")
        return None

# ------------------------------
# Glavni loop
# ------------------------------
async def check_loop():
    global old_content_hash
    await client.wait_until_ready()
    
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Greška: Kanal {CHANNEL_ID} nije pronađen!")
        return

    print(f"Monitoring pokrenut za kanal: {channel.name}")

    while not client.is_closed():
        new_page = await fetch_page()
        
        if new_page:
            # Uzimamo samo deo sadržaja ili hash radi stabilnosti
            # Ovde poredimo ceo text, ali koristimo hash da uštedimo memoriju
            current_hash = hash(new_page)

            if old_content_hash is not None and current_hash != old_content_hash:
                try:
                    await channel.send("🆕 **Novi mečevi su dodati na winpoint.gg!** @everyone")
                    print("Poruka poslata!")
                except Exception as e:
                    print(f"Greška pri slanju: {e}")
            
            old_content_hash = current_hash
        
        # Provera na svakih 5 minuta (bolje za Railway i manje šanse za Ban)
        await asyncio.sleep(300) 

@client.event
async def on_ready():
    print(f"Bot online: {client.user}")
    # Pokrećemo loop kao task
    client.loop.create_task(check_loop())

# Pokretanje
try:
    client.run(TOKEN)
except Exception as e:
    print(f"Bot se ugasio: {e}")
