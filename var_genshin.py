import discord
from discord import app_commands

import requests

data = requests.get("https://genshin.jmp.blue/characters").json()

color_visions = {
    "Anemo": 0x43cacd,
    "Cryo" : 0xa3eff7,
    "Dendro" : 0x9cff29,
    "Electro" : 0x661bbc,
    "Geo" : 0xc18c19,
    "Hydro" : 0x1f5fd5,
    "Pyro" : 0xfa4b2b
}

characters_choice= [app_commands.Choice(name = e.title(), value = e) for e in data]

# characters = []

# # print(characters)



def embed_character(id : str, long : bool = False) -> discord.Embed:

    data=requests.get(f"https://genshin.jmp.blue/characters/{id}").json()


    embed=discord.Embed(title=f"**{data.get('name', '')}**\n{data.get('title', '')}", color=color_visions[data.get('vision', '')])
    # embed.set_thumbnail(url=f"https://genshin.jmp.blue/elements/{data.get('vision', '')}/icon")


    embed.description=data["description"]
    embed.set_thumbnail(url=f"https://genshin.jmp.blue/characters/{id}/icon-big")

    if long:
        for skills in data.get('skillTalents',[]):
            embed.add_field(name=f"**{skills.get('name', '')}**",value=skills.get('description', ''),inline=False)


    return embed



embed_characterlist=discord.Embed(
    color=discord.Colour.blurple(),
    description="",
    title="Liste des personnages"
)
for e in requests.get("https://genshin.jmp.blue/characters").json():
    embed_characterlist.description+=e+"\n"