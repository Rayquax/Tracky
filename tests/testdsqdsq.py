@tree.command(name="test", description="t")
async def test(inte : discord.Interaction): 
    embed=discord.Embed(
        color=discord.Colour.dark_magenta(),
        description="test",
        title="testtitle",
    )
    file=discord.File('images/Radiant_Rank.png',filename='image.png')
    embed.set_image(url='attachements://image.png')
    
    await inte.response.send_message(embed=embed,file=file)
    time.sleep(10)
    embed1=discord.Embed(
        color=discord.Colour.dark_grey(),
        description="testamerelapute",
        title="tdsqdoqd",
    )
    await inte.edit_original_response(embed=embed1)
    '''
    liste_membres=inte.guild.members
    print(type(liste_membres))
    # liste_membres_id=[]
    # for elem in liste_membres:
    #     liste_membres_id.append(elem.id)
    
    
    with open('infos.json', "r") as f:
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
