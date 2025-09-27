# Contribution guidelines
## License
NekoBot is licensed under the GNU AGPL 3.0 license. As such, all contributions must be made under the same license or a compatible license. By making a contribution to this repository, you agree that your contribution may be used under the terms of the AGPL 3.0 and you assert that you are legally able to do so.

**Preference**: Either put your contribution(s) under AGPL itself, or a permissive license that allows it to be included under the AGPL (such as MIT or Apache).

## AI-generated Code
AI-generated code is forbidden from this project until the debate regarding how licensing even works with AI-generated code is finished and we have a concrete decision. Overall, at the moment LLMs seem like a font for license-laundering (especially with regards to copyleft and other non-permissive licenses) and the risk is simply not worth it.

This is not a ban on code / features *related* to AI, just a ban on code / features *written* by AI. It **is** entirely permitted to PR a change that adds a command to generate an image using an AI api, it is **not** permitted for that command to be written by ChatGPT, Claude, Google Gemini, or any other variety of AI coding assistant.

By submitting a contribution to this repository, you certify that none of the code in your contribution was created using an LLM or any other form of AI.

**In Summary**: No vibecoding

## General Code Guidelines
- Prefer to not use libraries outside of the Python Standard Library and the dependencies of Discord.Py as much as possible
  - Hence why the helper functions were written for this project, instead of using API wrapper libraries
  - Cuts down on the dependency list considerably, making it easier to run
- Prefer APIs that do not require accounts / authentication tokens to call
  - Rule34 is the current exception because creating an account there is fairly simple and it's a very important API
  - Making all these accounts would be a burden upon anyone running the bot, and we're not giving out the accounts and API keys
    - For one thing, giving them out is usually against ToS on the API platforms
- Try not to leak your own bot token / API keys, for your own sake ;P

### Static Artwork / Images
If you are submitting original artwork, say to replace one of the static images in `/resources/images`, we ask that you please license it under a license such as CC-BY-SA 4.0, CC-BY 4.0, CC0, or some other suitable license for the purpose. That way usage rights are clearly established, and we move a bit closer to being as FOSS as possible ^-^

However, we also recognize that finding suitably licensed anime-style images is... rather difficult. As such, we also will accept additions like those originally in the folder. We will also accept replacing one non-licensed image with another (so, for example, replacing one screenshot of an anime with another). We will *not*, however, accept replacing a properly-licensed image with an unlicensed one.

**In summary:** We would love to have properly licensed images for the commands that use static images! But we also recognize that finding them can be really difficult if you don't draw them yourself or commission someone yourself.
