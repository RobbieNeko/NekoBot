import discord
from discord.ext import commands
import json
from random import choice

from helper_funcs import *

with open("./config.json") as f:
    config = json.load(f)
    # discord.Object throws an error if fed a None, so ternary handles it gracefully
    MY_GUILD = discord.Object(id=config['guild-id']) if config['guild-id'] != None else None
    MY_TOKEN = config['bot-token']
    UNSPLASH_TOKEN = config['unsplash-token']

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
async def beer(interaction:discord.Interaction, target: discord.User | None = None):
    """Give someone a beer!"""
    if (target == None) or (target == interaction.user):
        await interaction.response.send_message("All alone? Aww, I'll share a beer with you :beer:")
    elif target == bot.user:
        await interaction.response.send_message(f"Thanks for the beer, {interaction.user.mention}! ^-^ :beer:")
    else:
        await interaction.response.send_message(f"{target.mention}, you just got a :beer: from {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def birb(interaction: discord.Interaction):
    """Display a birb!"""
    img, src = await unsplash_image('bird', UNSPLASH_TOKEN)
    if (img != ""):
        emb = discord.Embed(title="Birb Photo from Unsplash", description=f"Image by {src}")
        emb.set_image(url=img)
        await interaction.response.send_message(embed=emb)
    else:
        await interaction.response.send_message("Uh oh, looks like all the birbs are hiding! (Either the person running the bot has the wrong / no token set, or the API is getting ratelimited.)")

@bot.tree.command(guild=MY_GUILD)
async def bite(interaction: discord.Interaction, target: discord.User | None = None):
    """Bite someone >:3"""
    if target == None:
        await interaction.response.send_message("Are you trying to bite the air...?")
    else:
        if target == bot.user:
            await interaction.response.send_message("I-I'm not food! Don't bite me!! ;-;")
        elif target == interaction.user:
            await interaction.response.send_message("W-why would you want to... bite yourself?")
        else:
            link = await safebooru_image("biting+(+(+1girl+1boy+)+~+2girls+~+2boys+)")
            img = await file_from_url(link, "bite.png")
            await interaction.response.send_message(f"{target.mention}, you just got bitten by{interaction.user.mention}!", file=img)

@bot.tree.command(guild=MY_GUILD)
async def blush(interaction: discord.Interaction):
    """Post a blushing anime girl o///o"""
    link = await safebooru_image("blush+1girl+solo")
    img = await file_from_url(link, "blush.png")
    await interaction.response.send_message( file=img )

@bot.tree.command(guild=MY_GUILD)
async def boot(interaction: discord.Interaction, target: discord.User | None = None):
    """Throw a boot at someone! >:)"""
    # This represents what a command with multiple possible responses to a given prompt looks like
    with open("./resources/responses/boot.json") as file:
        resp = json.load(file)
        if target == None:
            await interaction.response.send_message(choice(resp['none']))
        else:
            if target == bot.user:
                await interaction.response.send_message(choice(resp['bot']))
            elif target == interaction.user:
                await interaction.response.send_message(choice(resp['self']))
            else:
                txt = choice(resp['someone'])
                await interaction.response.send_message(txt.replace("USER", interaction.user.display_name).replace("TARGET", target.display_name))

@bot.tree.command(guild=MY_GUILD)
async def botsupport(interaction:discord.Interaction):
    """Links to the bot's server!"""
    # FIXME: Update with actual server later
    if (interaction.guild == None) or (interaction.guild_id != 526466889380003851): # REPLACE WITH SUPPORT SERVER ID
        await interaction.response.send_message(f"Here you go {interaction.user.mention}: discord.gg/SUPPORTSERVERINVITEHERE")
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you're already in my home silly~ :heart:")

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=MY_GUILD)

bot.run(MY_TOKEN)



