import discord
from discord.ext import commands
import json
from random import choice

from helper_funcs import *

# Class added for customizability, namely the setup hook override
class NekoBot(commands.Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        # Sets things up, namely the global session
        self.session = aiohttp.ClientSession()

safebooru_meta = {
    "2people": "( ( 1girl 1boy ) ~ 2girls ~ 2boys )" # Actually means >= 2 people, not exactly 2 people
}

with open("./config.json") as f:
    config = json.load(f)
    # discord.Object throws an error if fed a None, so ternary handles it gracefully
    MY_GUILD = discord.Object(id=config['guild-id']) if config['guild-id'] != None else None
    MY_TOKEN = config['bot-token']
    UNSPLASH_TOKEN = config['unsplash-token']
    IMGFLIP_USER = config['imgflip-user']
    IMGLFIP_PASS = config['imgflip-pass']

intents = discord.Intents.default()
intents.message_content = True
bot = NekoBot(command_prefix="$", intents=intents)

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
            link = await safebooru_image(bot.session, ["1girl", "crying", "solo", "sad"])
            img = await file_from_url(bot.session, link, "crying_baka.png")
            await interaction.response.send_message("I-I'm not a baka, Y-YOU'RE A BAKA!! ;-;", file=img)
        elif target == interaction.user:
            img = discord.File("./resources/images/selfbaka.jpg")
            await interaction.response.send_message("You're such a baka you just called yourself a baka!", file=img)
        else:
            link = await safebooru_image(bot.session, ["pointing_at_another", safebooru_meta["2people"]])
            img = await file_from_url(bot.session, link, "baka.png")
            await interaction.response.send_message(f"{interaction.user.mention} just called {target.mention} a baka!", file=img)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to give a beer (optional)" )
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
    img, src = await unsplash_image(bot.session, 'bird', UNSPLASH_TOKEN)
    if (img != ""):
        emb = discord.Embed(title="Birb Photo from Unsplash", description=f"Image by {src}")
        emb.set_image(url=img)
        await interaction.response.send_message(embed=emb)
    else:
        await interaction.response.send_message("Uh oh, looks like all the birbs are hiding! (Either the person running the bot has the wrong / no token set, or the API is getting ratelimited.)")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
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
            link = await safebooru_image(bot.session, ["biting", safebooru_meta["2people"]])
            img = await file_from_url(bot.session, link, "bite.png")
            await interaction.response.send_message(f"{target.mention}, you just got bitten by {interaction.user.mention}!", file=img)

@bot.tree.command(guild=MY_GUILD)
async def blush(interaction: discord.Interaction):
    """Post a blushing anime girl o///o"""
    link = await safebooru_image(bot.session, ["blush", "1girl", "solo"])
    img = await file_from_url(bot.session, link, "blush.png")
    await interaction.response.send_message( file=img )

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
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

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(txt1="'Top Text' of the meme" )
@discord.app_commands.describe(txt2="'Bottom Text' of the meme (optional)" )
async def calling(interaction: discord.Interaction, txt1: str, txt2: str | None = None):
    """Generates a Tom & Jerry 'calling' meme"""
    if txt2 == None:
        link = await imgflip_meme(bot.session, 109538217, IMGFLIP_USER, IMGLFIP_PASS, txt1)
    else:
        link = await imgflip_meme(bot.session, 109538217, IMGFLIP_USER, IMGLFIP_PASS, txt1, txt2)
    
    img = await file_from_url(bot.session, link, 'calling.png')
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def cat(interaction: discord.Interaction):
    """Posts a random cat image! :3"""
    url = await nekoslife_url(bot.session, 'meow')
    img = await file_from_url(bot.session, url, 'cat.png')
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(choices="A string of choices, with each choice separated by a |" )
async def choose(interaction: discord.Interaction, choices: str | None = None):
    if choices == None:
        await interaction.response.send_message("You didn't give me any choices to pick from...") # Is this even possible?
    else:
        choicesList = choices.split('|')
        with open("./resources/responses/choose.json") as f:
            j = json.load(f)
            resp = choice(j)
            chose = choice(choicesList)
            await interaction.response.send_message(resp.replace('$X', chose))
        
@bot.tree.command(guild=MY_GUILD)
async def coffee(interation:discord.Interaction):
    """Sends a coffee image"""
    url = await flipnoteAPIs(bot.session, "https://coffee.alexflipnote.dev/random.json")
    img = await file_from_url(bot.session, url, "coffee.png")

    await interation.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def coinflip(interaction:discord.Interaction):
    """Flips a coin, for all your flipping needs!"""
    await interaction.response.send_message(f"{interaction.user.mention} flipped a coin and got {choice(['Heads', 'Tails'])}")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def cookie(interaction:discord.Interaction, target:discord.User | None = None):
    """Give someone a cookie :3"""
    if target == None:
        await interaction.response.send_message("Are you trying to give the air a cookie...?")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"T-thank you for the cookie {interaction.user.mention}! ^-^")
        elif target == interaction.user:
            await interaction.response.send_message(f"Um... c-could I get a piece of your cookie, {interaction.user.mention}?")
        else:
            await interaction.response.send_message(f"{target.mention}, you just got given a :cookie: by {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def cry(interaction: discord.Interaction):
    """Post a crying anime girl for when you're sad ._."""
    link = await safebooru_image(bot.session, ["crying", "1girl", "solo", "sad"])
    img = await file_from_url(bot.session, link, "crying.png")
    await interaction.response.send_message( file=img )

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def cuddle(interaction:discord.Interaction, target:discord.User | None = None):
    """Cuddle up to someone ^-^"""
    if target == None:
        await interaction.response.send_message("I don't think that's the right kind of 'void' to be cuddling...")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"*Cuddles {interaction.user.display_name} back* :3")
        elif target == interaction.user:
            await interaction.response.send_message(f"Aww, sorry to see you're all alone {interaction.user.mention} ;-;")
        else:
            link = await safebooru_image(bot.session, ["cuddling", safebooru_meta["2people"]])
            img = await file_from_url(bot.session, link, "cuddle.png")
            await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just cuddled up with you!", file=img)

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=MY_GUILD)

bot.run(MY_TOKEN)



