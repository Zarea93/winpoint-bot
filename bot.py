import discord
from discord.ext import tasks
import aiohttp
import os
from flask import Flask
from threading import Thread

# --- MINIMALNI WEB SERVER ---
app = Flask('')
@app.route('/')
def home():
    return "Bot je online!"

def run_web():
    # Railway će automatski dodeliti PORT, mi ga samo slušamo
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- TVOJI PODACI (DIREKTNO) ---
TOKEN = "OVDE_ZALEPI_SVOJ_NOVI_TOKEN"
CHANNEL_ID = 123456789012345678  # OVDE ZALEPI BROJ KANALA (BEZ NAVODNIKA)

class WinpointBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.old_hash = None

    async def setup_hook(self):
        self.check_site.start()

    async def on_ready(self):
        print(f'STATUS: Bot je uspesno povezan kao {self.user}')

    @tasks.loop(minutes=5)
    async def check_site(self):
        channel = self.get_channel(CHANNEL_ID)
        if not channel: return
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            async with aiohttp.ClientSession() as session:
                async with session.get("https://winpoint.gg", headers=headers, timeout=15) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        curr_hash = hash(text)
                        if self.old_hash is not None and curr_hash != self.old_hash:
                            await channel.send("🆕 **Novi mečevi na winpoint.gg!** @everyone")
                        self.old_hash = curr_hash
        except:
            pass

# --- POKRETANJE SVEGA ---
if __name__ == "__main__":
    # 1. Pokrećemo web server u posebnom "thread-u" (pozadini)
    t = Thread(target=run_web)
    t.start()
    
    # 2. Pokrećemo bota
    bot = WinpointBot()
    bot.run(TOKEN)
