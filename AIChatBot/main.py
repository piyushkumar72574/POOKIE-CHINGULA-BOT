import discord
import openai
import os

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)

# Memory to store which channel is AI for each server
ai_channels = {}

@bot.event
async def on_ready():
    await tree.sync()
    print(f"🤖 AI Chat Bot ready as {bot.user}")

@tree.command(name="setaichannel", description="Set this channel for AI replies")
async def set_channel(interaction: discord.Interaction):
    ai_channels[interaction.guild_id] = interaction.channel_id
    await interaction.response.send_message("✅ This channel is now set for AI auto-replies.", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild and ai_channels.get(message.guild.id) == message.channel.id:
        try:
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.content}]
            )
            await message.reply(reply.choices[0].message.content)
        except Exception as e:
            await message.channel.send("❌ Error from OpenAI: " + str(e))

bot.run(TOKEN)
