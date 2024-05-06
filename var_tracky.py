from discord import app_commands # type: ignore
import discord # type: ignore

import requests, random, json, os

import var_global

config_file = "config-bot.json"



lang="fr-FR"

langs_choice = [
    app_commands.Choice(name="Arabic (UAE)", value="ar-AE"),
    app_commands.Choice(name="German", value="de-DE"),
    app_commands.Choice(name="English", value="en-US"),
    app_commands.Choice(name="Spanish (Spain)", value="es-ES"),
    app_commands.Choice(name="Spanish (Mexico)", value="es-MX"),
    app_commands.Choice(name="French", value="fr-FR"),
    app_commands.Choice(name="Indonesian", value="id-ID"),
    app_commands.Choice(name="Italian", value="it-IT"),
    app_commands.Choice(name="Japanese", value="ja-JP"),
    app_commands.Choice(name="Korean", value="ko-KR"),
    app_commands.Choice(name="Polish", value="pl-PL"),
    app_commands.Choice(name="Portuguese (Brazil)", value="pt-BR"),
    app_commands.Choice(name="Russian", value="ru-RU"),
    app_commands.Choice(name="Thai", value="th-TH"),
    app_commands.Choice(name="Turkish", value="tr-TR"),
    app_commands.Choice(name="Vietnamese", value="vi-VN"),
    app_commands.Choice(name="Chinese (China)", value="zh-CN"),
    app_commands.Choice(name="Chinese (Taiwan)", value="zh-TW")
]

regions_choice = [
    app_commands.Choice(name = "Europe", value = "eu"),
    app_commands.Choice(name = "North America", value = "na"),
    app_commands.Choice(name = "Latin America", value = "latam"),
    app_commands.Choice(name = "Korea", value = "kr"),
    app_commands.Choice(name = "Brazil", value = "br"),
    app_commands.Choice(name = "Asia-Pacific", value = "ap")
]

characters_choice=[]

for c in requests.get(f"https://valorant-api.com/v1/agents?isPlayableCharacter=true&language=en-US").json().get('data', []): 
    characters_choice.append(app_commands.Choice(name = c['displayName'], value = c['uuid']))

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




def random_embed_character():
    requete=f"https://valorant-api.com/v1/agents?isPlayableCharacter=true&language={lang}"
    data=requests.get(requete).json()
    character=random.choice(data['data'])
    return embed_character(character, False)


def embed_by_id(id, long=True):
    c=requests.get(f"https://valorant-api.com/v1/agents/{id}?language={lang}").json()
    return embed_character(c['data'], long) if c['status']!=404 else var_global.embed_error


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
            title=f"{character.get('displayName', '')}"
        )
        embed.set_thumbnail(url=character['displayIcon'])


    return embed


def set_lang(language):
    lang=language

def load_config():
    global lang
    global token

    if not os.path.exists(config_file):
        config = {
            "lang": "fr-FR",
            "token": ""
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)

    else:
        with open("config-bot.json", "r") as f:
            config = json.load(f)

    lang=config['lang']
    token=config['token']

    if token=="":
        raise Exception("Please enter your TOKEN in config-bot.json")

    if lang not in [c.value for c in langs_choice]:
        raise Exception("Please enter a valid language in config-bot.json")



load_config()

