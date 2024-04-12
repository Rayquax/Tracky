from discord import app_commands
import discord


regions = [
    app_commands.Choice(name = "Europe", value = "eu"),
    app_commands.Choice(name = "North America", value = "na"),
    app_commands.Choice(name = "Latin America", value = "latam"),
    app_commands.Choice(name = "Korea", value = "kr"),
    app_commands.Choice(name = "Brazil", value = "br"),
    app_commands.Choice(name = "Asia-Pacific", value = "ap")
]

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