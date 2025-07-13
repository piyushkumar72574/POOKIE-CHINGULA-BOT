import discord
from discord.ext import tasks
import aiohttp
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# Store which channel to send memes in each server
meme_channels = {}

@bot.event
async def on_ready():
    await tree.sync()
    send_meme.start()
    print(f"😂 MemeBot logged in as {bot.user}")

@tree.command(name="setmemechannel", description="Set this channel for automatic Hindi memes")
async def set_meme_channel(interaction: discord.Interaction):
    meme_channels[interaction.guild_id] = interaction.channel_id
    await interaction.response.send_message("✅ This channel is now set for Hindi meme auto-posting.", ephemeral=True)

@tasks.loop(minutes=30)
async def send_meme():
    for guild_id, channel_id in meme_channels.items():
        channel = bot.get_channel(channel_id)
        if channel:
            meme_url = await get_meme()
            if meme_url:
                await channel.send(meme_url)

async def get_meme():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme/IndianDankMemes") as resp:
                data = await resp.json()
                return data.get("url")
    except Exception as e:
        print("Error getting meme:", e)
        return None

bot.run(TOKEN)
