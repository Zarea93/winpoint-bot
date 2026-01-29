import discord
from discord.ext import tasks
import aiohttp
import os
import sys

# --- DEBUG SEKCIJA ---
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("--- PROVERA SISTEMA ---")
print(f"Python verzija: {sys.version}")
print(f"Da li je TOKEN pronadjen: {'DA' if TOKEN else 'NE'}")
print(f"Vrednost CHANNEL_ID: {CHANNEL_ID}")
print("-----------------------")

if not TOKEN or not CHANNEL_ID:
    print("ERROR: Varijable nisu ucitane! Proveri Railway panel.")
    # Necemo raise-ovati error odmah da bot ne bi stalno restartovao u krug
    # vec cemo ga pustiti da stoji upaljen kako bi mogao da procitas logove
    TOKEN = "RESTARTUJ_ME" 

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.old_hash = None

    async def setup_hook(self):
        self.check_website.start()

    @tasks.loop(minutes=5)
    async def check_website(self):
        if not self.is_ready() or TOKEN == "RESTARTUJ_ME":
            return
        
        channel = self.get_channel(int(CHANNEL_ID))
        if channel:
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://winpoint.gg", headers=headers, timeout=15) as resp:
                        if resp.status == 200:
                            html = await resp.text()
                            new_hash = hash(html)
                            if self.old_hash is not None and new_hash != self.old_hash:
                                await channel.send("🆕 **Novi mečevi na winpoint.gg!** @everyone")
                            self.old_hash = new_hash
            except Exception as e:
                print(f"Greška: {e}")

bot = MyBot()
try:
    bot.run(TOKEN)
except Exception as e:
    print(f"Bot nije mogao da se pokrene: {e}")
