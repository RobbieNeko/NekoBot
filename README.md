# NekoBot

NekoBot is a Discord bot largely inspired by [this version of KawaiiBot](https://github.com/KawaiiBot/KawaiiBot) and coded in Python with the Discord.Py library! I was a big fan of KawaiiBot in the past, and was saddened when the primary developer first ended the original bot, and then in the new version axed the NSFW commands and took the bot's new code (funnily enough, they also apparently chose to do it in Python) private. I also got interested in learning how to make a Discord bot in general, and I thought it'd be a fun little project, so I decided to make NekoBot!

NekoBot has aimed to have the vast majority of the commands in the original KawaiiBot included, and of the commands that didn't make it, most are due to either using private APIs I don't have a replacement for (yet) or general unreliable APIs. However, I believe that it would be great to not just be a replacement for the old version of KawaiiBot, but to grow even better than it! As such, PRs for additional commands / expanding existing commands and overall improving the bot are very welcome! Just be sure to read the [contribution notes](./CONTRIBUTING.md).

Contributions don't have to just be code! They can also be expanding the list of options in the files in `/resources/responses`, adding to the list of 'banned tags' for imageboard APIs, or submitting artwork! We especially would love to have some properly licensed artwork / images to replace those in `/resources/images` that are currently just anime screenshots and the like.

## Requirements
Requirements to run the bot period:
- [discord.py](https://github.com/Rapptz/discord.py)
  - And its dependencies (namely, aiohttp)
- The Python Standard Library
  - json, random, base64, io (BytesIO)
- Python 3.13 or newer
  - Must support `type1 | type2` style syntax for Unions
  - Versions less than 3.13 seem to run into some syntax errors regarding parentheses
- A discord bot account with token

Requirements to have certain commands functional:
- Rule 34
  - Rule 34 API key and user id

### Final notes
NekoBot is licensed under the AGPL 3.0 license

We politely ask that any copyright or licensing issues/concerns be brought up with the project lead before jumping **straight** to DMCA notices and other threats. Trust us, we want to remedy those issues just as quickly as you do!
