import discord
import aiohttp
from discord.ext import commands

# FIXME Remove for final deployment, this is just for testing purposes
MY_GUILD = discord.Object(id='INSERT YOUR ID HERE (as an integer)')
MY_TOKEN = 'INSERT YOUR BOT TOKEN HERE (but keep it private for your own sake)'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.tree.command(guild=MY_GUILD)
async def about(interaction: discord.Interaction):
    """Prints basic 'about' info"""
    info = discord.Embed(title='About Nekobot')
    info.add_field(name="Developer(s)", value="RosaAeterna (aka NekoRobbie)")
    info.add_field(name="Library", value="Discord.py")
    info.add_field(name="License", value="GNU GPL v3")
    await interaction.response.send_message(embed=info)

@bot.tree.command(guild=MY_GUILD)
async def avatar(interaction: discord.Interaction):
    """Shows your avatar"""
    disp = discord.Embed(description=f"{interaction.user.display_name}'s Avatar\n[Full Image]({interaction.user.display_avatar.url})")
    disp.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=disp)

@bot.tree.command(guild=MY_GUILD)
async def testimage(interaction:discord.Interaction):
    """Posts a test image"""
    await interaction.response.send_message("https://img4.gelbooru.com/images/31/2f/312fc11a21c5d4ce06dc3aa8bfbb7221.jpg")

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=MY_GUILD)

bot.run(MY_TOKEN)



