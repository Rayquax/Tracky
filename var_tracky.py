from discord import app_commands
import discord

import requests


lang="fr-FR"

regions = [
    app_commands.Choice(name = "Europe", value = "eu"),
    app_commands.Choice(name = "North America", value = "na"),
    app_commands.Choice(name = "Latin America", value = "latam"),
    app_commands.Choice(name = "Korea", value = "kr"),
    app_commands.Choice(name = "Brazil", value = "br"),
    app_commands.Choice(name = "Asia-Pacific", value = "ap")
]

characters=[]

for c in requests.get(f"https://valorant-api.com/v1/agents?isPlayableCharacter=true&language={lang}").json().get('data', []): 
    characters.append(app_commands.Choice(name = c['displayName'], value = c['uuid']))



ranks = ['Radiant','Immortal','Ascendant','Diamond','Platinum','Gold','Silver','Bronze','Iron']

colors={
    'Radiant':0xf9e6ad,
    'Immortal':0xA32D3E,
    'Ascendant':0x4b8333,
    'Diamond':0x9989c9,
    'Platinum':0xB0E0E6,
    'Gold':0xf3ce5a,
    'Silver' :0xe5deda,
    'Bronze':0x936536,
    'Iron':0x6b6b6b
}


embed_wait=discord.Embed(
    color=discord.Colour.blurple(),
    title="🔄"
)

embed_error=discord.Embed(
    color=discord.Colour.red(),
    title="❌",
)

embed_ok=discord.Embed(
    color=discord.Colour.green(),
    title="✅"
)


def random_embed_character():
    requete=f"https://valorant-api.com/v1/agents?isPlayableCharacter=true&language={lang}"
    data=requests.get(requete).json()
    character=random.choice(data['data'])
    return random.choice(characters)


def embed_character(character, long=False):



    if long:
        embed=discord.Embed(
            color=discord.Colour(int(character.get('backgroundGradientColors',[0])[0][:-2], 16)),
            title=f"{character.get('displayName', '')} - *{character.get('role', '').get('displayName', '')}*",
            # description=f"{character.get('description', '')}",
        )
        embed.set_thumbnail(url=character['displayIcon'])

        for e in character.get('abilities',[]):
            embed.add_field(name=f"**{e.get('displayName', '')}**",value=e.get('description', ''),inline=False)

    else:
        embed=discord.Embed(
            color=discord.Colour(int(character.get('backgroundGradientColors',[0])[0][:-2], 16)),
            title=f"{character.get('displayName', '')} - *{character.get('role', '').get('displayName', '')}*"
        )
        embed.set_image(url=character['displayIcon'])


    return embed