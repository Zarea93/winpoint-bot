import discord
from discord.ext import tasks
import aiohttp

# --- OVDE DIREKTNO UPIŠI ---
TOKEN = "MTQ2NjMzNjk5MDEyNjQwNzczMQ.GDcRPU.lfvPqspEXkLwAl9eIiKF5oiXlBkgVmgNfXjxJs"
CHANNEL_ID = 123456789012345678  # 1365627989987033098
# ---------------------------

class WinpointBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.old_hash = None

    async def setup_hook(self):
        self.check_site.start()

    async def on_ready(self):
        print(f'USPEH! Bot je online kao: {self.user}')

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
                            await channel.send("🆕 **New matches are added on winpoint.gg!** @everyone")
                        self.old_hash = curr_hash
        except:
            pass

bot = WinpointBot()
bot.run(TOKEN)
