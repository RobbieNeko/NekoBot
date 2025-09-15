import discord
from discord.ext import commands

from helper_funcs import *

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
@discord.app_commands.describe(target="User you want to target (optional)" )
async def baka(interaction: discord.Interaction, target: discord.User|None = None):
    """Calls the target a baka!"""
    if target == None: #Funny little response like the original
        await interaction.response.send_message("Who are you trying to call a baka...?")
    else:
        if target == bot.user:
            link = await safebooru_image("1girl+crying+solo+sad")
            img = await file_from_url(link, "crying_baka.png")
            await interaction.response.send_message("I-I'm not a baka, Y-YOU'RE A BAKA!! ;-;", file=img)
        elif target == interaction.user:
            img = discord.File("./resources/images/selfbaka.jpg")
            await interaction.response.send_message("You're such a baka you just called yourself a baka!", file=img)
        else:
            link = await safebooru_image("pointing_at_another+(+(+1girl+1boy+)+~+2girls+~+2boys+)")
            img = await file_from_url(link, "baka.png")
            await interaction.response.send_message(f"{interaction.user.mention} just called {target.mention} a baka!", file=img)

@bot.tree.command(guild=MY_GUILD)
async def testimage(interaction:discord.Interaction):
    """Posts a test image"""
    await interaction.response.send_message("https://img4.gelbooru.com/images/31/2f/312fc11a21c5d4ce06dc3aa8bfbb7221.jpg")

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=MY_GUILD)

bot.run(MY_TOKEN)



