import discord
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"⚙️ CoreBot ready as {bot.user}")

@tree.command(name="hello", description="Test command to say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("👋 Hello! I'm alive and working.", ephemeral=True)

@tree.command(name="ping", description="Check if bot is online")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong! Bot is online.", ephemeral=True)

bot.run(TOKEN)
