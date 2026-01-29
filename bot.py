import discord
from discord.ext import tasks
import aiohttp
import os

# ČITANJE PODATAKA IZ RAILWAY-A (Ne diraj ovo)
TOKEN = os.getenv("TOKEN")
try:
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except:
    CHANNEL_ID = None

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
        if not self.is_ready() or not CHANNEL_ID:
            return
        channel = self.get_channel(CHANNEL_ID)
        if not channel:
            print(f"GRESKA: Kanal sa ID {CHANNEL_ID} nije pronadjen!")
            return
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            async with aiohttp.ClientSession() as session:
                async with session.get("https://winpoint.gg", headers=headers, timeout=15) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        curr_hash = hash(text)
                        if self.old_hash is not None and curr_hash != self.old_hash:
                            await channel.send("🆕 **New matches are added on winpoint.gg!** @everyone")
                        self.old_hash = curr_hash
        except Exception as e:
            print(f"Greska pri proveri sajta: {e}")

bot = WinpointBot()
if TOKEN:
    bot.run(TOKEN)
else:
    print("FATALNA GRESKA: TOKEN varijabla nije pronadjena u Railway panelu!")
