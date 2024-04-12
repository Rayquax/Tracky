import discord
import requests
import json
from discord.ext import commands
from discord import app_commands
# from discord.utils import get
import time
import class_tracky

















intents = discord.Intents.all()



bot = commands.Bot(command_prefix='-', intents=intents)

tree = bot.tree


    



@bot.event
async def on_ready():
    await tree.sync()
    print("Done")
    print(f'Connecte en tant que {bot.user.name}')







regions = [
    app_commands.Choice(name = "Europe", value = "eu"),
    app_commands.Choice(name = "North America", value = "na"),
    app_commands.Choice(name = "Latin America", value = "latam"),
    app_commands.Choice(name = "Korea", value = "kr"),
    app_commands.Choice(name = "Brazil", value = "br"),
    app_commands.Choice(name = "Asia-Pacific", value = "ap")
]

ranks = [
    'Radiant',
    'Immortal',
    'Ascendant',
    'Diamond',
    'Platinum',
    'Gold',
    'Silver',
    'Bronze',
    'Iron']

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


@tree.command(name="val-config-roles", description="Créer les roles")
async def vcr(inte : discord.Interaction, separated : bool = True):
    
    await inte.response.send_message('🔄',ephemeral=True)
    
    
    with open('roles.json', "r") as f:
        dico_serv_roles=json.load(f)
    
    if dico_serv_roles[str(inte.guild_id)]:
        for name in dico_serv_roles[str(inte.guild_id)]:
            role = discord.utils.get(inte.guild.roles, id=dico_serv_roles[str(inte.guild.id)][str(name)])
            try: await role.delete() 
            except: pass
    
    
    
    
    dico_serv_roles[str(inte.guild_id)]={}
    for rank in ranks:
        role = await inte.guild.create_role(name=rank,mentionable=True,hoist=separated,color=discord.Colour(colors[rank]))
        dico_serv_roles[str(inte.guild_id)][str(rank)]=role.id

    with open('roles.json', "w") as f:
        json.dump(dico_serv_roles, f, indent=2)
    
    await inte.edit_original_response(content='✅')
    
    
    

    

@tree.command(name="val-delete-roles", description="Supprimer les roles")
async def vdr(inte : discord.Interaction):
    
    
    await inte.response.send_message("🔄",ephemeral=True)
    with open('roles.json', "r") as f:
        dico_serv_roles=json.load(f)
    
    for name in dico_serv_roles[str(inte.guild_id)]:
        role = discord.utils.get(inte.guild.roles, id=dico_serv_roles[str(inte.guild.id)][str(name)])
        await role.delete()
    
    
    dico_serv_roles[str(inte.guild_id)]={}
    with open('roles.json', "w") as f:
        json.dump(dico_serv_roles, f, indent=2)
        
    await inte.edit_original_response(content='✅')
    
    





@tree.command(name="val-search-rank", description="Avoir le rang d'un joueur")
@app_commands.choices(region=regions)
async def vsr(inte : discord.Interaction, pseudo : str, tag : str, region : app_commands.Choice[str] = 'eu'):
    
    
    await inte.response.send_message("🔄")
    try:
        region=region if type(region)==str else region.value
        
        
        Player=class_tracky.Joueur(pseudo,tag,region)
        await Player.send_rank(inte)
    except:
        await inte.edit_original_response("❌")
        raise

    
    
    




@tree.command(name="val-set-pseudo", description="Sauvegarder son pseudo et son id (avec la region par défaut sur eu)")
@app_commands.choices(region=regions)
async def vsp(inte : discord.Interaction, pseudo : str, tag : str, region : app_commands.Choice[str]='eu'):
    region=region if type(region)==str else region.value
    uid = inte.user.id
    await inte.response.send_message("🔄",ephemeral=True)
    if uid==None:
        await inte.edit_original_response("❌")
    else:
        with open('info-val.json', "r") as f:
            dico_usr=json.load(f)
        dico_usr[str(uid)]={
                'pseudo':pseudo,
                'tag':tag,
                'region':region
            }
        with open('info-val.json', "w") as f:
            json.dump(dico_usr, f, indent=2)
        await inte.edit_original_response(content='✅')


  


    
@tree.command(name="val-get-rank", description="Avoir le rang d'un joueur du serveur (non spécifié)")
async def vgr(inte : discord.Interaction, membre: discord.Member = None):
    embed = discord.Embed(
        title='Titre de l\'embed',
        description='Description de l\'embed',
        color=discord.Color.blue()
        )

        # Ajoutez une image à l'embed
        
        
    # file = discord.File('images/Diamond_1_Rank.png', filename='Diamond_1_Rank.png')
    embed.set_image(url='attachment://Diamond_1_Rank.png')
    # embed.set_image(url='images/Diamond_1_Rank.png')
        
    await inte.response.send_message("🔄",embed=embed)
    
    time.sleep(2)
    # embed.set_image(url='images/Diamond_2_Rank.png')
    
    try:
        
        guild=inte.guild
        uid = inte.user.id if membre is None else membre.id
        
        
        
        
        with open('info-val.json', "r") as f:
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
                with open('roles.json', "r") as f:
                    dico_serv_roles=json.load(f)

                for role_usr in inte.user.roles:
                    for rank in ranks:
                        
                        if role_usr.id == dico_serv_roles[str(guild.id)][rank]:
                            await inte.user.remove_roles(role_usr)
                role = discord.utils.get(guild.roles, id=dico_serv_roles[str(guild.id)][str(Player.get_rank()[0])])
                
                await inte.user.add_roles(role)
               
            except: raise
        
        
    except:
        await inte.edit_original_response(content="❌")
        raise


    
@tree.command(name="val-top-rank", description="Montrer le top rank du serveur")
async def tr(inte : discord.Interaction):
    await inte.response.send_message("🔄")
    try:
        with open('info-val.json', "r") as f:
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
    
    
    '''
    liste_membres=inte.guild.members
    print(type(liste_membres))
    # liste_membres_id=[]
    # for elem in liste_membres:
    #     liste_membres_id.append(elem.id)
    
    
    with open('info-val.json', "r") as f:
        dico_usr=json.load(f)
    
    
    for index,usr in enumerate(liste_membres):
        if usr.id not in dico_usr:
            liste_membres.remove(usr)
        else:
            pseudo=dico_usr[str(usr.id)]["pseudo"]
            tag=dico_usr[str(usr.id)]["tag"]
            region=dico_usr[str(usr.id)]["region"]
            
            liste_membres[index]=class_tracky.Joueur(pseudo,tag,region)
    liste_membres.sort()
    for i in liste_membres:
        print(i)
    '''



# Démarrer le bot
bot.run("MTA5MjE0MTA5OTk1MjM3ODAwOQ.GxozaG.6MZmWq3YhbCCf7ybT_2M01CsArQN0amcncitQI")
