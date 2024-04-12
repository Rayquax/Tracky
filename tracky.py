import discord
# import requests
import json
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import time

from numpy import var


import class_tracky
import var_tracky















intents = discord.Intents.all()



bot = commands.Bot(command_prefix='-', intents=intents)

tree = bot.tree






@bot.event
async def on_ready():
    await tree.sync()
    print("Done")
    print(f'Connecte en tant que {bot.user.name}')









@tree.command(name="config_roles", description="Créer les roles")
async def cr(inte : discord.Interaction, separated : bool = True):
    
    await inte.response.send_message('🔄',ephemeral=True)
    
    
    with open('data/roles.json', "r") as f:
        dico_serv_roles=json.load(f)
    
    if dico_serv_roles[str(inte.guild_id)]:
        for name in dico_serv_roles[str(inte.guild_id)]:
            role = discord.utils.get(inte.guild.roles, id=dico_serv_roles[str(inte.guild.id)][str(name)])
            try: await role.delete() 
            except: pass
    
    
    
    
    dico_serv_roles[str(inte.guild_id)]={}
    for rank in var_tracky.ranks:
        role = await inte.guild.create_role(name=rank,mentionable=True,hoist=separated,color=discord.Colour(var_tracky.colors[rank]))
        dico_serv_roles[str(inte.guild_id)][str(rank)]=role.id

    with open('data/roles.json', "w") as f:
        json.dump(dico_serv_roles, f, indent=2)
    
    await inte.edit_original_response(embed=var_tracky.embed_ok)


@tree.command(name="delete_roles", description="Créer les roles")
async def dr(inte : discord.Interaction):
    
    
    await inte.response.send_message("🔄",ephemeral=True)
    with open('data/roles.json', "r") as f:
        dico_serv_roles=json.load(f)
    
    for name in dico_serv_roles[str(inte.guild_id)]:
        role = discord.utils.get(inte.guild.roles, id=dico_serv_roles[str(inte.guild.id)][str(name)])
        await role.delete()
    
    
    dico_serv_roles[str(inte.guild_id)]={}
    with open('data/roles.json', "w") as f:
        json.dump(dico_serv_roles, f, indent=2)
        
    await inte.edit_original_response(content='✅')


@tree.command(name="search_rank", description="Avoir le rang d'un joueur")
@app_commands.choices(region=var_tracky.regions)
async def sr(inte : discord.Interaction, pseudo : str, tag : str, region : app_commands.Choice[str] = 'eu'):
    
    
    await inte.response.send_message(embed=var_tracky.embed_wait)
    try:
        region=region if type(region)==str else region.value
        
        
        Player=class_tracky.Joueur(pseudo,tag,region)
        await Player.send_rank(inte)
    except:
        await inte.edit_original_response("❌")
        raise


@tree.command(name="set_pseudo", description="Sauvegarder son pseudo et son id (avec la region par défaut sur eu)")
@app_commands.choices(region=var_tracky.regions)
async def sp(inte : discord.Interaction, pseudo : str, tag : str, region : app_commands.Choice[str]='eu'):
    region=region if type(region)==str else region.value
    uid = inte.user.id
    
    await inte.response.send_message(embed=var_tracky.embed_wait,ephemeral=True)
    if uid==None:
        await inte.edit_original_response("❌")
    else:
        with open('data/infos.json', "r") as f:
            dico_usr=json.load(f)
        dico_usr[str(uid)]={
                'pseudo':pseudo,
                'tag':tag,
                'region':region
            }
        with open('data/infos.json', "w") as f:
            json.dump(dico_usr, f, indent=2)
        await inte.edit_original_response(content='✅')

    
@tree.command(name="get_rank", description="Avoir le rang d'un joueur du serveur (non spécifié=soi même)")
async def gr(inte : discord.Interaction, membre: discord.Member = None):
    
    await inte.response.send_message("",embed=var_tracky.embed_wait)
    
    try:
        
        guild=inte.guild
        uid = inte.user.id if membre is None else membre.id
        

        with open('data/infos.json', "r") as f:
            dico_usr=json.load(f)
        pseudo=dico_usr.get(str(uid), {}).get("pseudo")
        tag=dico_usr.get(str(uid),{}).get("tag")
        region=dico_usr.get(str(uid),{}).get("region")

        if pseudo is None:
            print("Pseudo non trouvé")
        else:
            Player=class_tracky.Joueur(pseudo,tag,region)
            await Player.send_rank(inte)
        
        if membre is None:
            try:
                with open('data/roles.json', "r") as f:
                    dico_serv_roles=json.load(f)

                for role_usr in inte.user.roles:
                    if role_usr.id in dico_serv_roles[str(guild.id)]:
                        await inte.user.remove_roles(role_usr)
                    # for rank in ranks:
                        # if role_usr.id == dico_serv_roles[str(guild.id)][rank]:
                        #     await inte.user.remove_roles(role_usr)
                role = discord.utils.get(guild.roles, id=dico_serv_roles[str(guild.id)][str(Player.rank)])
                
                await inte.user.add_roles(role)

            except: raise
        
        
    except:
        await inte.edit_original_response(embed=var_tracky.embed_error)
        raise


    
@tree.command(name="top_rank", description="Montrer le top rank du serveur")
async def tr(inte : discord.Interaction):
    
    
    await inte.response.send_message(embed=var_tracky.embed_wait)
    try:
        with open('data/infos.json', "r") as f:
            dico_usr=json.load(f)
        
        liste_membres=[]
        for uid in dico_usr:
            user=inte.guild.get_member(int(uid))
            if user!= None:
                pseudo=dico_usr[str(uid)]["pseudo"]
                tag=dico_usr[str(uid)]["tag"]
                region=dico_usr[str(uid)]["region"]
                
                
                liste_membres.append((class_tracky.Joueur(pseudo,tag,region),user))
        liste_membres.sort(reverse=True)
        res=''
        for num,player in enumerate(liste_membres):
            res+=f'{num+1}: {player[1].name} {player[0]}\n'
        await inte.edit_original_response(content=res)
    except:
        await inte.edit_original_response(content="❌")
        raise



# Démarrer le bot
bot.run("MTA5MjE0MTA5OTk1MjM3ODAwOQ.GxozaG.6MZmWq3YhbCCf7ybT_2M01CsArQN0amcncitQI")
