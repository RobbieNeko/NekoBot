import discord
import aiohttp
from io import BytesIO

type Link = str
type Attribution = str


async def safebooru_image(session:aiohttp.ClientSession, tags: list[str]) -> Link:
    """Returns either a URL to an image on safebooru, 'Empty', or an HTTP error code number (as string)"""
    baseurl = "https://safebooru.org/index.php"
    # Using parameters instead of manually constructing the string for the sake of example / trying it out
    par = {
        "page": "dapi",
        "s": "post",
        "q": "index",
        "json": '1',
        "tags": ' '.join(['sort:random'] + tags) # Joining with + gets escaped, but joining with spaces gets made into joining with +. WHY HTTP, WHY.
    }

    async with session.get(baseurl, params=par) as response:
        if response.status == 200:
            img = await response.json()
            if img != {}:
                return img[0]['file_url']
            else:
                return 'Empty'
        else:
            return f'{response.status}'

async def http_error_handler(error:str) -> str:
    """Returns an error message depending on the HTTP error code"""
    code = int(error)

    match code:
        case 400:
            return "Uh oh, the website didn't like your request, but we don't know why! Please contact the person who is running the bot and report the issue!"
        case 401 | 403:
            return "The request is Forbidden or I don't have permission to see it. Please contact the person who is running the bot and report the issue!"
        case 404:
            return "I can't find the webpage you were looking for! Please report this to the person running the bot."
        case 408:
            return "The request timed out! Please try again in a little bit, and report the issue if it persists."
        case 418:
            return "I can't find the website you were looking for... but I found a teapot! Would you like some chai?"
        case 500:
            return "Uh oh, the website doesn't seem to be responding correctly! Maybe try again in a little bit, after it hopefully wakes up?"
        case 502:
            return "Uh oh, looks like the gateway and the website are arguing right now. Maybe come back a little later, and hope that they've worked out their issues?"
        case 503:
            return "The website is busy right now, so try again a little bit later."
        case 504:
            return "Uh oh, looks like the gateway can't get a response out of the website right now. Try again later?"
        case _:
            return "Unrecognized HTTP error recieved! Please alert the bot developer so they can start handling it."

async def file_from_url(session:aiohttp.ClientSession, url:str, name: str)-> discord.File:
    """Constructs a file from a URL using aiohttp and BytesIO.
    'name' should contain a file extension because Discord doesn't do mimetype/magic numbers"""
    async with session.get(url) as response:
        buffer = BytesIO(await response.read())
    return discord.File(fp=buffer, filename=name)

async def unsplash_image(session:aiohttp.ClientSession, searchTerm: str, apiToken: str) -> tuple[Link, Attribution]:
    """Fetches an image from unsplash
    Prefer practically any other API when possible"""
    baseurl = f"https://api.unsplash.com/photos/random/?client_id={apiToken}"
    searchurl = baseurl + f"&query={searchTerm}"
    # Not using parameters here because this is such a simple one

    async with session.get(searchurl) as response:
        if response.status == 200:
            img = await response.json()
            return (img['urls']['regular'], img['user']['name'])
        else:
            return ("","")

async def imgflip_meme(session:aiohttp.ClientSession, id:int, user:str, pword:str, txt1:str ="", txt2:str ="") -> Link:
    """Generates a meme from imgflip
    `id` has to be manually obtained from URLs, txt1 is top txt, txt2 is bottom txt"""
    url = "https://api.imgflip.com/caption_image"
    d = {
        "template_id":id,
        "username":user,
        "password":pword,
        "text0": txt1,
        "text1": txt2
        }

    async with session.post(url, data=d) as resp:
        if resp.status == 200:
            j = await resp.json()
            if j['success']:
                return j['data']['url']
            else:
                return f"Request Failed: {j['error_message']}"
        else:
            return f"{resp.status}"

async def nekoslife_url(session: aiohttp.ClientSession, endpoint:str) -> str:
    """Hits an endpoint at nekoslife
    `endpoint` must be from the list on https://github.com/Nekos-life/nekos-dot-life """

    urlEndpoints = ["smug", "baka", "tickle", "slap", "poke", "pat", "neko", "ngif", "meow", "lizard", "kiss", "hug", "fox_girl", "feed", "cuddle", "kemonomimi", "holo", "wallpaper", "goose", "gecg", "avatar", "waifu"]
    txtEndpoints = ["why", "cat"],
    spclEndpoints = ['owoify', "8ball", "chat", "fact", "spoiler"]
    
    if endpoint in spclEndpoints:
        return "Special Endpoints are currently unsupported"

    if (endpoint in urlEndpoints) or endpoint == "eightball":
        url = "https://nekos.life/api/v2/img/"
    else:
        url = "https://nekos.life/api/v2/"
    url += endpoint
    
    async with session.get(url) as response:
        if response.status == 200:
            j = await response.json()
            if endpoint in urlEndpoints:
                return j['url']
            else:
                match endpoint:
                    case "cat":
                        return j['cat']
                    case "why":
                        return j['why']
                    case "owoify":
                        return j['owo']
                    case "fact":
                        return j['fact']
                    case "8ball":
                        return j['response']
                    case _:
                        # This just means we forgot to define the behavior for an endpoint somewhere
                        # Eventually this should just be a case of "process of elimination'd option"
                        return "Undefined endpoint response"
        else:
            print(f"Response: {response.status}")
            return "Recieved some HTTP error"

async def flipnoteAPIs(session: aiohttp.ClientSession, api: Link) -> str:
    """ Hits up an original alexflipnote API.
    Because hey, might as well politely use it and avoid stuff like Unsplash"""

    async with session.get(api) as response:
        if response.status == 200:
            j = await response.json()
            return j['file']
        else:
            print(f"Response: {response.status}")
            return 'Recieved some HTTP error'
