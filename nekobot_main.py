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

with open("./config.json") as file:
    config = json.load(file)
    # discord.Object throws an error if fed a None, so ternary handles it gracefully
    MY_GUILD = discord.Object(id=config['guild-id']) if config['guild-id'] != None else None
    MY_TOKEN = config['bot-token']
    SUPPORT_INVITE = config['support-server-link']
    FEEDBACK_CHANNEL = config['feedback-channel-id']

with open("./resources/banned_tags.json") as file:
    # Banned because Discord doesn't like them, and in many countries they could get you in hot water
    BANNED_TAGS = json.load(file)

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
    url = await flipnoteAPIs(bot.session, "https://api.alexflipnote.dev/birb")
    img = await file_from_url(bot.session, url, 'birb.png')
    await interaction.response.send_message(file=img)

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
        await interaction.response.send_message(f"Here you go {interaction.user.mention}: {SUPPORT_INVITE}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you're already in my home silly~ :heart:")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(txt="Text of the meme" )
async def calling(interaction: discord.Interaction, txt: str):
    """Generates a Tom & Jerry 'calling' meme"""
    # This one returns an image directly instead of a link
    img = await file_from_url(bot.session, f"https://api.alexflipnote.dev/calling?&text={txt}", 'calling.png')
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

@bot.tree.command(guild=MY_GUILD)
async def dab(interaction: discord.Interaction):
    """Dab on the haters"""
    link = await safebooru_image(bot.session, ["dab_(dance)", "solo"])
    emb = discord.Embed(description=choice(["Dabs on the haters", "Dabbing is sooo 2016", "#DabNeverDied"]))
    emb.set_image(url=link)
    await interaction.response.send_message( embed=emb )

@bot.tree.command(guild=MY_GUILD)
async def dance(interaction: discord.Interaction):
    """Posts a dancing anime image so you can boogie"""
    link = await safebooru_image(bot.session, ["dancing"])
    img = await file_from_url(bot.session, link, "dancing.png")
    await interaction.response.send_message( file=img )

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(txt1="Text in the searchbar" )
@discord.app_commands.describe(txt2="'Did you mean to search for' text under searchbar" )
async def didyoumean(interation:discord.Interaction, txt1: str, txt2:str):
    """Sends an image of a search asking if you meant something else"""
    # Directly returns image
    img = await file_from_url(bot.session, f"https://api.alexflipnote.dev/didyoumean?&top={txt1}&bottom={txt2}", "didyoumean.png")

    await interation.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def dog(interaction: discord.Interaction):
    """Display a dog!"""
    url = await flipnoteAPIs(bot.session, "https://api.alexflipnote.dev/dogs")
    img = await file_from_url(bot.session, url, 'dog.png')
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def doot(interaction: discord.Interaction):
    """Doot!"""
    img = discord.File("./resources/images/doot.gif")
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(txt1="Top text" )
@discord.app_commands.describe(txt2="Bottom text" )
async def drake(interation:discord.Interaction, txt1: str, txt2:str):
    """Makes a drake meme"""
    # Direct file return
    img = await file_from_url(bot.session, f"https://api.alexflipnote.dev/drake?&top={txt1}&bottom={txt2}", "drake.png")

    await interation.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def duck(interaction: discord.Interaction):
    """Returns a random duck!"""
    # This one returns an image directly instead of a link
    img = await file_from_url(bot.session, f"https://random-d.uk/api/v2/randomimg", 'duck.png')
    await interaction.response.send_message(file=img)

@bot.tree.command(guild = MY_GUILD, nsfw=True)
@discord.app_commands.describe(tags="A list of tags, separated by spaces." )
async def e621(interaction: discord.Interaction, tags: str):
    """Searches E621 and returns a random post matching your tags!"""
    # Assumes the user knows how e621 tags work
    tagList = tags.split()
    for tag in tagList:
        for ban in BANNED_TAGS:
            # This catches substrings too, otherwise it'd be shockingly easy to bypass
            if ban in tag:
                await interaction.response.send_message("Uh oh, your list of tags contained a tag for content that Discord TOS does not permit!\nSorry, but I can't help you with this search >.>")
    
    link = await e621API(bot.session, tagList)
    # All the error messages do not start with 'h'
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, "e621.png")
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild = MY_GUILD)
async def echo(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"{interaction.user.mention}: {text}")

@bot.tree.command(guild=MY_GUILD)
async def eightball(interaction: discord.Interaction, question: str):
    """Asks the magic 8ball a question!"""
    link = await nekoslife_url(bot.session, f"8ball", f"text={question}")
    img = await file_from_url(bot.session, link, '8ball.png')
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def f(interaction: discord.Interaction, reason: str | None = None):
    """Press F to pay respects"""
    heart_colors: list[str] = ["pink", "red", "orange", "yellow", "green", "light_blue", "blue", "purple"]
    if reason == None:
        await interaction.response.send_message(f"{interaction.user.mention} just paid their respects :{choice(heart_colors)}_heart:")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} just paid their respects for {reason} :{choice(heart_colors)}_heart:")

@bot.tree.command(guild=MY_GUILD)
async def facts(interaction:discord.Interaction, text:str):
    """Makes whatever you say into a fact!"""
    # Directly returns image
    img = await file_from_url(bot.session, f"https://api.alexflipnote.dev/facts?text={text}", "facts.png")
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(feedback="Feedback! Please remember that you're sending this to a person :3" )
async def feedback(interaction:discord.Interaction, feedback: str):
    """Sends feedback to the person running the bot!"""
    # Unsure if I actually prefer this or github issues tbh
    channel = bot.get_channel(FEEDBACK_CHANNEL)
    if type(channel) == discord.TextChannel:
        await channel.send(feedback)
        await interaction.response.send_message("Feedback sent!", ephemeral=True)
    else:
        await interaction.response.send_message("Uh oh, it looks like the person running the bot didn't set the feedback channel correctly!\nAnd... you can't report it to them using the feedback command.\nSo, um, I guess find them yourself? Sorry I can't be more helpful ;-;")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def flower(interaction: discord.Interaction, target: discord.User | None = None) :
    """Give someone a flower!"""
    # French is convenient for avoiding name collision ;P
    fleur = choice(['blossom', 'cherry_blossom', 'hibiscus', 'hyacinth', 'lotus', 'rose', 'sunflower', 'tulip'])
    
    if target == None:
        await interaction.response.send_message("Um... are you trying to give the floor a flower?")
    elif target == interaction.user:
        await interaction.response.send_message(f"Oh, no-one's given you flowers before? ... here, I'll be the first! :{fleur}:")
    elif target == bot.user:
        await interaction.response.send_message(f"Awww, thanks for the flower {interaction.user.mention}! ^//^ :{fleur}:")
    else:
        await interaction.response.send_message(f"{target.mention}, you just got a :{fleur}: from {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def fruit(interaction: discord.Interaction, target: discord.User | None = None) :
    """Give someone some fruit!"""
    froot = choice(['red_apple', 'cherries', 'banana', 'grapes', 'kiwi', 'lime', 'mango', 'melon', 'pear', 'pineapple', 'tangerine', 'watermelon', 'lemon', 'peach'])
    
    if target == None:
        await interaction.response.send_message("Um... are you trying to leave an offering to the spirits?")
    elif target == interaction.user:
        await interaction.response.send_message(f"Um, {interaction.user.mention}... can I have some of your :{froot}:? It looks really tasty!")
    elif target == bot.user:
        await interaction.response.send_message(f"Oooh, thanks for the :{froot}: {interaction.user.mention}! It's really juicy ^-^")
    else:
        await interaction.response.send_message(f"{target.mention}, you just got a :{froot}: from {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def funfact(interaction: discord.Interaction):
    """Get a fun fact!"""
    fact = await nekoslife_url(bot.session, "fact")
    await interaction.response.send_message("Fun fact: " + fact)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def handholding(interaction:discord.Interaction, target:discord.User | None = None):
    """Engage in some handholding! :3"""
    if target == None:
        await interaction.response.send_message("Um... are you trying to hold the hand of a ghost?")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"*Holds {interaction.user.display_name}'s hand back* :3")
        elif target == interaction.user:
            await interaction.response.send_message(f"Aww, sorry to see you're all alone {interaction.user.mention} ;-;")
        else:
            link = await safebooru_image(bot.session, ["holding_hands", safebooru_meta["2people"]])
            img = await file_from_url(bot.session, link, "handholding.png")
            await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just held hands with you!", file=img)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def highfive(interaction:discord.Interaction, target:discord.User | None = None):
    """High five someone!"""
    if target == None:
        await interaction.response.send_message("Was there a fly or something? Why were you swatting at the air?")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"Hecc yeah! High-five {interaction.user.mention}! :folded_hands:")
        elif target == interaction.user:
            await interaction.response.send_message(f"Um... {interaction.user.mention}, I think that's called clapping, not a self-high-five >.>")
        else:
            link = await safebooru_image(bot.session, ["high_five", safebooru_meta["2people"]])
            img = await file_from_url(bot.session, link, "highfive.png")
            await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just high-fived you!", file=img)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def hug(interaction:discord.Interaction, target:discord.User | None = None):
    """Hug someone ^//^"""
    if target == None:
        await interaction.response.send_message("Are you... trying to grab the air?")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"*Hugs {interaction.user.display_name} back* :heart:")
        elif target == interaction.user:
            img = discord.File("./resources/images/selfhug.gif")
            await interaction.response.send_message(f"Aww, sorry to see you're all alone {interaction.user.mention} ;-;", file=img)
        else:
            link = await safebooru_image(bot.session, ["hug", safebooru_meta["2people"]])
            img = await file_from_url(bot.session, link, "hug.png")
            await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just hugged you!", file=img)

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=MY_GUILD)

bot.run(MY_TOKEN)



