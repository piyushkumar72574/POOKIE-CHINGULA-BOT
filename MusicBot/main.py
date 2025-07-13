import discord
from discord.ext import commands
import wavelink
import os

TOKEN = os.getenv("DISCORD_TOKEN")
LAVALINK_URL = os.getenv("LAVALINK_URL")
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    await wavelink.NodePool.create_node(
        bot=bot,
        host=LAVALINK_URL.split(":")[0],
        port=int(LAVALINK_URL.split(":")[1]),
        password=LAVALINK_PASSWORD,
        https=False
    )

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect(cls=wavelink.Player)
        await ctx.send("Joined voice channel!")
    else:
        await ctx.send("Join a VC first!")

@bot.command()
async def play(ctx, *, search: str):
    player: wavelink.Player = ctx.voice_client

    if not player:
        await ctx.send("Bot is not in VC.")
        return

    track = await wavelink.YouTubeTrack.search(search, return_first=True)
    await player.play(track)
    await ctx.send(f"Now playing: {track.title}")

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()
    await ctx.send("Left voice channel.")

bot.run(TOKEN)
