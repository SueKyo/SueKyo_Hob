import discord
from discord import Intents
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
SCHEDULED_TIME = os.getenv('SCHEDULED_TIME')
REACTION_CHECK_DELAY = 60 * 60 * 5 # Delay (in seconds) before checking for reactions

intents = Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {bot.user.name}')
    auto_post.start()

@tasks.loop(seconds=60)
async def auto_post():
    channel = bot.get_channel(CHANNEL_ID)
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    current_day = now.weekday()
    tomorrow = now + timedelta(days=1)
    tomorrow_date = tomorrow.strftime('%m月%d日')

    if current_time == SCHEDULED_TIME and current_day not in (4, 5):
        message = await channel.send(f"明日（{tomorrow_date}）学校来る人✋")
        await asyncio.sleep(REACTION_CHECK_DELAY)  # Wait for the specified time

        # Check reactions after the specified time
        message = await channel.fetch_message(message.id)
        total_reactions = sum([reaction.count for reaction in message.reactions])
        if total_reactions == 0:
            await channel.send("とっても残念です。")

bot.run(TOKEN)
