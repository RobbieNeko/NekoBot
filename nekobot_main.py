import discord
from discord.ext import commands
import json
import random

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

# Change this to whatever your source code's link is, if you run a modified version
SOURCE_CODE_URL = "https://github.com/RobbieNeko/NekoBot"

with open("./config.json") as file:
    config = json.load(file)
    # discord.Object throws an error if fed a None, so ternary handles it gracefully
    MY_GUILD = discord.Object(id=config['guild-id']) if config['guild-id'] != None else None
    MY_TOKEN = config['bot-token']
    SUPPORT_INVITE = config['support-server-link']
    FEEDBACK_CHANNEL = config['feedback-channel-id']
    BOT_INVITE = config['bot-invite-link']

with open("./resources/banned_tags.json") as file:
    # Banned because Discord doesn't like them, and in many countries they could get you in hot water
    BANNED_TAGS = json.load(file)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = NekoBot(command_prefix="$", intents=intents)

@bot.tree.command(guild=MY_GUILD)
async def about(interaction: discord.Interaction):
    """Prints basic 'about' info"""
    info = discord.Embed(title='About NekoBot')
    info.add_field(name="Developer(s)", value="RosaAeterna (aka NekoRobbie)")
    info.add_field(name="Library", value="Discord.py")
    info.add_field(name="License", value="GNU AGPL v3")
    info.add_field(name="Inspiration", value="KawaiiBot (kotlin version)")
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
            link = await nekosbest_url(bot.session, 'cry')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "crying.gif")
                await interaction.response.send_message("I-I'm not a baka, Y-YOU'RE A BAKA!! ;-;", file=img)
            else:
                # Unlike a lot of situations, this doesn't actually need to print the error
                await interaction.response.send_message("I-I'm not a baka, Y-YOU'RE A BAKA!! ;-;")
        elif target == interaction.user:
            img = discord.File("./resources/images/selfbaka.jpg")
            await interaction.response.send_message("You're such a baka you just called yourself a baka!", file=img)
        else:
            link = await nekosbest_url(bot.session, 'baka')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "baka.gif")
                await interaction.response.send_message(f"{interaction.user.mention} just called {target.mention} a baka!", file=img)
            else:
                await interaction.response.send_message(f"{interaction.user.mention} just called {target.mention} a baka!")

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
    link = await flipnoteAPIs(bot.session, "https://api.alexflipnote.dev/birb")
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, 'birb.png')
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link) # Actually sends error message

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
            link = await nekosbest_url(bot.session, 'bite')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "bite.gif")
                await interaction.response.send_message(f"{target.mention}, you just got bitten by {interaction.user.mention}!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, you just got bitten by {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def blush(interaction: discord.Interaction):
    """Post a blushing anime girl o///o"""
    link = await nekosbest_url(bot.session, "blush")
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, "blush.gif")
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def boot(interaction: discord.Interaction, target: discord.User | None = None):
    """Throw a boot at someone! >:)"""
    # This represents what a command with multiple possible responses to a given prompt looks like
    with open("./resources/responses/boot.json") as file:
        resp = json.load(file)
        if target == None:
            await interaction.response.send_message(random.choice(resp['none']))
        else:
            if target == bot.user:
                await interaction.response.send_message(random.choice(resp['bot']))
            elif target == interaction.user:
                await interaction.response.send_message(random.choice(resp['self']))
            else:
                txt = random.choice(resp['someone'])
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
    # This does mean that there is no error handling
    img = await file_from_url(bot.session, f"https://api.alexflipnote.dev/calling?&text={txt}", 'calling.png')
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def cat(interaction: discord.Interaction):
    """Posts a random cat image! :3"""
    link = await nekoslife_url(bot.session, 'meow')
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, 'cat.png')
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(choices="A string of choices, with each choice separated by a |" )
async def choose(interaction: discord.Interaction, choices: str | None = None):
    if choices == None:
        await interaction.response.send_message("You didn't give me any choices to pick from...") # Is this even possible?
    else:
        choicesList = choices.split('|')
        with open("./resources/responses/choose.json") as f:
            j = json.load(f)
            resp = random.choice(j)
            chose = random.choice(choicesList)
            await interaction.response.send_message(resp.replace('$X', chose))
        
@bot.tree.command(guild=MY_GUILD)
async def coffee(interaction:discord.Interaction):
    """Sends a coffee image"""
    link = await flipnoteAPIs(bot.session, "https://coffee.alexflipnote.dev/random.json")
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, "coffee.png")
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
async def coinflip(interaction:discord.Interaction):
    """Flips a coin, for all your flipping needs!"""
    await interaction.response.send_message(f"{interaction.user.mention} flipped a coin and got {random.choice(['Heads', 'Tails'])}")

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
    link = await nekosbest_url(bot.session, 'cry')
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, "crying.gif")
        await interaction.response.send_message( file=img )
    else:
        await interaction.response.send_message(link)

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
            link = await nekosbest_url(bot.session, 'cuddle')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "cuddle.gif")
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just cuddled up with you!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just cuddled up with you!")

@bot.tree.command(guild=MY_GUILD)
async def dab(interaction: discord.Interaction):
    """Dab on the haters"""
    link = await safebooru_image(bot.session, ["dab_(dance)", "solo"])
    if link[0] == 'h':
        emb = discord.Embed(description=random.choice(["Dabs on the haters", "Dabbing is sooo 2016", "#DabNeverDied"]))
        emb.set_image(url=link)
        await interaction.response.send_message(embed=emb)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
async def dance(interaction: discord.Interaction):
    """Posts a dancing anime image so you can boogie"""
    link = await nekosbest_url(bot.session, 'dance')
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, "dancing.gif")
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

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
    link = await flipnoteAPIs(bot.session, "https://api.alexflipnote.dev/dogs")
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, 'dog.png')
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

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
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, '8ball.png')
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
async def f(interaction: discord.Interaction, reason: str | None = None):
    """Press F to pay respects"""
    heart_colors: list[str] = ["pink", "red", "orange", "yellow", "green", "light_blue", "blue", "purple"]
    if reason == None:
        await interaction.response.send_message(f"{interaction.user.mention} just paid their respects :{random.choice(heart_colors)}_heart:")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} just paid their respects for {reason} :{random.choice(heart_colors)}_heart:")

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
    fleur = random.choice(['blossom', 'cherry_blossom', 'hibiscus', 'hyacinth', 'lotus', 'rose', 'sunflower', 'tulip'])
    
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
    froot = random.choice(['red_apple', 'cherries', 'banana', 'grapes', 'kiwi', 'lime', 'mango', 'melon', 'pear', 'pineapple', 'tangerine', 'watermelon', 'lemon', 'peach'])
    
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
            link = await nekosbest_url(bot.session, 'handhold')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "handholding.gif")
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just held hands with you!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just held hands with you!")

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
            link = await nekosbest_url(bot.session, 'highfive')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "highfive.gif")
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just high-fived you!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just high-fived you!")

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
            link = await nekoslife_url(bot.session, 'hug')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "hug.gif")
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just hugged you!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just hugged you!")

@bot.tree.command(guild=MY_GUILD)
async def invite(interaction: discord.Interaction):
    """Get an invite link to invite me to your server!"""
    # Note: You will start running into restrictions at 100 servers with the bot in them unless you verify.
    await interaction.response.send_message("Here's a link to invite me to your server!\n"+BOT_INVITE, ephemeral=True)

@bot.tree.command(guild=MY_GUILD)
async def joinedat(interaction: discord.Interaction, user: discord.Member):
    """Get the date that someone joined the server!"""
    await interaction.response.send_message(f"{user.display_name} joined {user.joined_at.strftime("%B %d, %Y") if user.joined_at != None else "before date and time were a thing! o.O"}")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def kiss(interaction:discord.Interaction, target:discord.User | None = None):
    """Kiss someone ^////^"""
    if target == None:
        await interaction.response.send_message("U-um... are you trying to blow a kiss at me? o//o")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"*Kisses {interaction.user.display_name} back* :heart: ^///^")
        elif target == interaction.user:
            await interaction.response.send_message(f"Aww, sorry to see you're all alone {interaction.user.mention} ;-;")
        else:
            link = await nekoslife_url(bot.session, 'kiss')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "kiss.gif")
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just kissed you!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, {interaction.user.mention} just kissed you!")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def lick(interaction:discord.Interaction, target:discord.User | None = None):
    """Lick someone o///o"""
    if target == None:
        await interaction.response.send_message("U-um... are you trying to lick the air?? o.o")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"{interaction.user.mention}... am I tasty or something?? o///o")
        elif target == interaction.user:
            await interaction.response.send_message(f"Are you... trying to lick yourself clean like a cat? o.o")
        else:
            link = await safebooru_image(bot.session, ["licking_another's_face", safebooru_meta["2people"]]) # Weird tag acquired straight from website search
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "lick.png")
                await interaction.response.send_message(f"{target.mention}, you just got licked by {interaction.user.mention}!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, you just got licked by {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def lovecalc(interaction: discord.Interaction, person1: discord.User, person2: discord.User):
    """Calculate the love between two people!"""
    if (person1 == person2) and (person1 == interaction.user):
        link = await nekoslife_url(bot.session, 'hug')
        if link[0] == 'h':
            img = await file_from_url(bot.session, link, "hug.gif")
            await interaction.response.send_message("W-wait... are you not sure if you love yourself or not???\nI'm so sorry to hear that ;-;", file=img)
        else:
            await interaction.response.send_message("W-wait... are you not sure if you love yourself or not???\nI'm so sorry to hear that ;-;")
    elif (person1 == bot.user and person2 == interaction.user) or (person2 == bot.user and person1 == interaction.user):
        link = await nekosbest_url(bot.session, "blush")
        if link[0] == 'h':
            img = await file_from_url(bot.session, link, 'blush.gif')
            await interaction.response.send_message(f"U-um, are you trying to tell me something {interaction.user.display_name}???", file=img)
        else:
            await interaction.response.send_message(f"U-um, are you trying to tell me something {interaction.user.display_name}???")
    elif (person1 == bot.user) or (person2 == bot.user):
        await interaction.response.send_message(f"{interaction.user}... are you trying to ship me and them?? >///>")
    else:
        love = random.Random(person1.id + person2.id)
        percent = love.randint(0, 100)

        emb = discord.Embed(title=":heart: Love Calculator :heart:", description=f"Love between {person1.mention} and {person2.mention} is at **{percent}%**")
        await interaction.response.send_message(embed=emb)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional, will default to you)" )
async def meme(interaction: discord.Interaction, top: str, bottom: str, target: discord.User | discord.Member | None = None):
    """Make a meme out of a user!"""
    if target == None:
        # Default to author
        target = interaction.user
    img = await memegen_img(bot.session, target.display_avatar.url, top, bottom)
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def nani(interaction: discord.Interaction):
    """Posts a confused anime girl"""
    # Not *exactly* the original command, but good enough
    link = await safebooru_image(bot.session, ["1girl", "solo", "confused"])
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, 'nani.png')
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
async def neko(interaction: discord.Interaction):
    """Posts a random neko image! :3"""
    link = await nekoslife_url(bot.session, 'neko')
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, 'neko.png')
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def nom(interaction:discord.Interaction, target:discord.User | None = None):
    """Nom someone! :3"""
    if target == None:
        await interaction.response.send_message("Um... are you trying to nom the air?")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"*Noms {interaction.user.display_name} back* :3")
        elif target == interaction.user:
            await interaction.response.send_message(f"Aww, sorry to see you're all alone {interaction.user.mention} ;-;")
        else:
            link = await nekosbest_url(bot.session, 'nom')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "nom.gif")
                await interaction.response.send_message(f"{target.mention}, you just got nommed by {interaction.user.mention}!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, you just got nommed by {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def notwork(interaction:discord.Interaction):
    """Tell someone 'That's not how it works you lil shit'!"""
    img = discord.File("./resources/images/notwork.png")
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def pat(interaction:discord.Interaction, target:discord.User | None = None):
    """Give someone headpats! ^-^"""
    if target == None:
        await interaction.response.send_message("Are you patting a ghost?")
    else:
        link = await nekoslife_url(bot.session, 'pat')
        if link[0] == 'h':
            img = await file_from_url(bot.session, link, "pat.gif")
            if target == bot.user:
                await interaction.response.send_message(f"Aww, thanks {interaction.user.mention}! ^//^", file=img)
            elif target == interaction.user:
                await interaction.response.send_message(f"Um... do you want me to give you headpats, {interaction.user.mention}?\n... because I'd be happy to :pink_heart:", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, you just got headpats from {interaction.user.mention}!", file=img)
        else:
            if target == bot.user:
                await interaction.response.send_message(f"Aww, thanks {interaction.user.mention}! ^//^")
            elif target == interaction.user:
                await interaction.response.send_message(f"Um... do you want me to give you headpats, {interaction.user.mention}?\n... because I'd be happy to :pink_heart:")
            else:
                await interaction.response.send_message(f"{target.mention}, you just got headpats from {interaction.user.mention}!",)

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def pickle(interaction: discord.Interaction, target: discord.User | discord.Member | None = None):
    """Find out someone's pickle size!"""
    # Sus command?
    if target == None:
        target = interaction.user
    rand = random.Random(target.id)
    size = rand.uniform(0.0, 50.0)
    if target == interaction.user:
        await interaction.response.send_message(f"{interaction.user.mention}, your pickle size is {size / 1.17:.2f}cm ^-^")
    elif target == bot.user:
        await interaction.response.send_message(f"M-my pickle size? U-um... {size / 1.17:.2f}cm >///>")
    else:
        await interaction.response.send_message(f"{target.display_name}'s pickle size is {size / 1.17:.2f}cm ^-^")

@bot.tree.command(guild=MY_GUILD)
async def ping(interaction: discord.Interaction):
    """Ping!"""
    # Maybe add actual ping information if it becomes relevant-er
    await interaction.response.send_message("Pong! :ping_pong:")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def poke(interaction:discord.Interaction, target:discord.User | None = None):
    """Poke someone! ^-^"""
    if target == None:
        await interaction.response.send_message("What are you trying to point to?")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"Don't poke me! ;-;")
        elif target == interaction.user:
            await interaction.response.send_message(f"Why are you poking yourself? ... you're not fat, {interaction.user.mention}! ;-;")
        else:
            link = await nekosbest_url(bot.session, 'poke')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "poke.gif")
                await interaction.response.send_message(f"{target.mention}, you just got poked by {interaction.user.mention}!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, you just got poked by {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def ratewaifu(interaction:discord.Interaction, waifu:str):
    """Rates your waifu~!"""
    rand = random.Random(waifu)
    rating = rand.uniform(0.0, 10.0)
    await interaction.response.send_message(f"I rate {waifu} {rating:.1f}/10 ^-^")

@bot.tree.command(guild=MY_GUILD)
async def reverse(interaction: discord.Interaction, text:str):
    """Reverses text, wow! !wow, txet sesreveR"""
    # String slicing goes brrrr
    await interaction.response.send_message(text[::-1])

@bot.tree.command(guild=MY_GUILD)
async def roll(interaction: discord.Interaction, min: int, max: int):
    """Rolls a number between min and max"""
    await interaction.response.send_message(f"{interaction.user.mention} rolled {min}-{max} and got **{random.randint(min,max)}**")

@bot.tree.command(guild=MY_GUILD)
async def rps(interaction: discord.Interaction, choice: str):
    """Rock paper scissors!"""
    choice = choice.lower()
    options = {"rock":"scissors", "paper":"rock", "scissors":"paper"}
    if choice == "gun":
        await interaction.response.send_message("Please don't shoot! It's just a game of Rock Paper Scissors! O.O")
    elif (choice == "lizard") or (choice == "spock"):
        await interaction.response.send_message("Sorry, this is Rock Paper Scissors, not Rock Paper Scissors Lizard Spock. I'd love to learn how to play that though! ^-^")
    elif choice in options:
        myChoice = random.choice(list(options.keys()))
        if choice == myChoice:
            await interaction.response.send_message(f"{choice} v.s. {myChoice}\nIt's a tie!")
        elif options[choice] == myChoice:
            await interaction.response.send_message(f"{choice} v.s. {myChoice}\nYou win {interaction.user.mention}! ^-^")
        else:
            await interaction.response.send_message(f"{choice} v.s. {myChoice}\nYou lose {interaction.user.mention}! ^-^")
    else:
        await interaction.response.send_message("You have to pick 'rock', 'scissors', or 'paper'!")

@bot.tree.command(guild = MY_GUILD, nsfw=True)
@discord.app_commands.describe(tags="A list of tags, separated by spaces." )
async def rule34(interaction: discord.Interaction, tags: str):
    """Searches rule34.xxx and returns a random post matching your tags!"""
    # Assumes the user knows how rule34 tags work
    tagList = tags.split()
    for tag in tagList:
        for ban in BANNED_TAGS:
            # This catches substrings too, otherwise it'd be shockingly easy to bypass
            if ban in tag:
                await interaction.response.send_message("Uh oh, your list of tags contained a tag for content that Discord TOS does not permit!\nSorry, but I can't help you with this search >.>")
    
    link = await rule34_image(bot.session, tagList)
    # All the error messages do not start with 'h'
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, "rule34.png")
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
async def scroll(interaction: discord.Interaction, text: str):
    """Post the scroll of truth!"""
    img = await file_from_url(bot.session, f"https://api.alexflipnote.dev/scroll?text={text}", 'scroll.png')
    await interaction.response.send_message(file=img)

@bot.tree.command(guild=MY_GUILD)
async def server(interaction: discord.Interaction):
    """Posts info about the server!"""
    if interaction.guild != None:
        guild = interaction.guild
        emb = discord.Embed(title=f"Information about {guild.name}")
        emb.add_field(name="Server name", value=guild.name)
        emb.add_field(name="Server ID", value=guild.id)
        emb.add_field(name="Members", value=guild.member_count)
        emb.add_field(name="Owner", value=guild.owner.display_name if guild.owner != None else "Unknown")
        if guild.icon != None:
            emb.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(embed=emb)
    else:
        await interaction.response.send_message("Sorry, I can't seem to figure out what guild you're in! o.o")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def slap(interaction:discord.Interaction, target:discord.User | None = None):
    """Slap someone! o.o"""
    if target == None:
        await interaction.response.send_message("Are you trying to fan yourself... or slap a ghost?")
    else:
        if target == bot.user:
            await interaction.response.send_message(f"Ow! Hey, why did you do that {interaction.user.mention}?!? ;-;")
        elif target == interaction.user:
            await interaction.response.send_message(f"{interaction.user.mention}, why are you slapping yourself?? o.o")
        else:
            link = await nekoslife_url(bot.session, 'slap')
            if link[0] == 'h':
                img = await file_from_url(bot.session, link, "slap.gif")
                await interaction.response.send_message(f"{target.mention}, you just got slapped by {interaction.user.mention}!", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, you just got slapped by {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def slots(interaction: discord.Interaction):
    """Play the slots!"""
    # No actual prizes included ;P
    icons = ['red_apple', 'cherries', 'tangerine', 'watermelon', 'lemon', 'peach']
    a, b, c = random.choices(icons, k=3)
    if (a == b == c):
        await interaction.response.send_message(f"{interaction.user.mention} just played the slots...\n:{a}: :{b}: :{c}:\n... and just won! ^-^")
    elif (a == b) or (a == c) or (b == c):
        await interaction.response.send_message(f"{interaction.user.mention} just played the slots...\n:{a}: :{b}: :{c}:\n... and nearly won! :3")
    else:
        await interaction.response.send_message(f"{interaction.user.mention} just played the slots...\n:{a}: :{b}: :{c}:\n... and lost.")

@bot.tree.command(guild=MY_GUILD)
async def source(interaction: discord.Interaction):
    """Get a link to the source code!"""
    # Any derivatives should change this to a link to their own code
    await interaction.response.send_message("Here's my source code! ^-^\n{SOURCE_CODE_URL}")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def throw(interaction:discord.Interaction, target: discord.User):
    """Throw an item at someone! >:3"""
    with open('./resources/responses/throw.json') as file:
        data = json.load(file)
        authorMsg = random.choice(data['author'])
        targetMsg = random.choice(data['target'])
        item = random.choice(data['items'])
    await interaction.response.send_message(f"{interaction.user.mention} just threw {item} at {target.mention}!\n**{interaction.user.display_name}:** {authorMsg}\n**{target.display_name}:** {targetMsg}")

@bot.tree.command(guild=MY_GUILD)
@discord.app_commands.describe(target="User you want to target (optional)" )
async def tickle(interaction:discord.Interaction, target:discord.User | None = None):
    """Tickle someone! ^///^"""
    if target == None:
        await interaction.response.send_message("Are you trying to tickle the void?")
    else:
        link = await nekoslife_url(bot.session, 'tickle')
        if link[0] == 'h':
            img = await file_from_url(bot.session, link, "tickle.gif")
            if target == bot.user:
                await interaction.response.send_message(f"*giggles* :pink_heart:", file=img)
            elif target == interaction.user:
                await interaction.response.send_message(f"{interaction.user.mention}, you do know that tickling yourself doesn't work... right?\nDo you want me to tickle you? :3", file=img)
            else:
                await interaction.response.send_message(f"{target.mention}, you just got tickled by {interaction.user.mention}!", file=img)
        else:
            if target == bot.user:
                await interaction.response.send_message(f"*giggles* :pink_heart:")
            elif target == interaction.user:
                await interaction.response.send_message(f"{interaction.user.mention}, you do know that tickling yourself doesn't work... right?\nDo you want me to tickle you? :3")
            else:
                await interaction.response.send_message(f"{target.mention}, you just got tickled by {interaction.user.mention}!")

@bot.tree.command(guild=MY_GUILD)
async def user(interaction: discord.Interaction):
    """Posts info about your account!"""
    user = interaction.user
    emb = discord.Embed(title=f"About {user.name}")
    emb.add_field(name="Base name", value=user.name)
    emb.add_field(name="Server name / nickname", value=user.display_name)
    emb.add_field(name="Account created", value=user.created_at.strftime("%B %d, %Y"))
    emb.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=emb)

@bot.tree.command(guild=MY_GUILD)
async def wag(interaction: discord.Interaction):
    """Post a tail-wagging image! ^-^"""
    link = await safebooru_image(bot.session, ["tail_wagging", "solo"])
    if link[0] == 'h':
        img = await file_from_url(bot.session, link, 'wag.png')
        await interaction.response.send_message(file=img)
    else:
        await interaction.response.send_message(link)

@bot.tree.command(guild=MY_GUILD)
async def woop(interaction: discord.Interaction):
    """Woop woop!"""
    img = discord.File("./resources/images/woop.gif")
    await interaction.response.send_message(file=img)

@bot.command()
async def sync(ctx):
    await bot.tree.sync(guild=MY_GUILD)

@bot.command()
async def changestatus(ctx, status):
    # Only the owner(s) should be able to do this
    if bot.is_owner(ctx.author):
        await bot.change_presence(activity=discord.Game(status))

bot.run(MY_TOKEN)



