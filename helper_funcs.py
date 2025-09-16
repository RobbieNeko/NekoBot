import discord
import aiohttp
from io import BytesIO

type Link = str
type Attribution = str

async def safebooru_image(tags: str) -> Link:
    """Returns either a URL to an image on safebooru, 'Empty', or an HTTP error code number (as string)"""
    baseurl = "https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&tags=sort:random+"
    searchurl = baseurl + tags

    async with aiohttp.ClientSession() as session:
        async with session.get(searchurl) as response:
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

async def file_from_url(url:str, name: str)-> discord.File:
    """Constructs a file from a URL using aiohttp and BytesIO.
    'name' should contain a file extension because Discord doesn't do mimetype/magic numbers"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            buffer = BytesIO(await response.read())
    return discord.File(fp=buffer, filename=name)

async def unsplash_image(searchTerm: str, apiToken: str) -> tuple[Link, Attribution]:
    baseurl = f"https://api.unsplash.com/photos/random/?client_id={apiToken}"
    searchurl = baseurl + f"&query={searchTerm}"

    async with aiohttp.ClientSession() as session:
        async with session.get(searchurl) as response:
            if response.status == 200:
                img = await response.json()
                return (img['urls']['regular'], img['user']['name'])
            else:
                return ("","")

async def imgflip_meme(id:int, user:str, pword:str, txt1:str ="", txt2:str ="") -> Link:
    url = "https://api.imgflip.com/caption_image"
    d = {
        "template_id":id,
        "username":user,
        "password":pword,
        "text0": txt1,
        "text1": txt2
        }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=d) as resp:
            if resp.status == 200:
                j = await resp.json()
                if j['success']:
                    return j['data']['url']
                else:
                    return f"Request Failed: {j['error_message']}"
            else:
                return f"{resp.status}"
