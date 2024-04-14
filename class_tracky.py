import requests
import discord
import var_tracky


ranks = ['Iron','Bronze','Silver','Gold','Platinum','Diamond','Ascendant','Immortal','Radiant']





class Joueur:
    def __init__(self, pseudo : str, tag : str, region : str) -> None:
        self.pseudo=pseudo
        self.tag=tag
        self.region=region
        self.valid=self.load_rank()

        #print(self.stats)
    
    def __repr__(self) -> str:
        Player_stats=self.stats
        if Player_stats[0]=='Radiant':
            return f"**{self.pseudo}**#{self.tag} : **{Player_stats[0]}** #{Player_stats[1]}"
        else:
            return f"**{self.pseudo}**#{self.tag} : **{Player_stats[0]} {Player_stats[1]}** {Player_stats[2]} RR"
    

    async def send_rank(self,inte):
        # with open('images/Radiant_Rank.png', 'rb') as f:
        #     image_data = f.read()
        
        self.embed_rank.set_thumbnail(url="attachment://image.png")
        
        
        await inte.edit_original_response(attachments=[self.file],embed=self.embed_rank)
        
    def load_rank(self):
        requete=f'https://api.kyroskoh.xyz/valorant/v1/mmr/{self.region}/{self.pseudo}/{self.tag}?show=combo&display=0'

        res=requests.get(requete).text.split(" ")
        
        if '-' in res : res.remove('-')
        
        while res[-1][-1] not in "0123456789":
            res[-1]=res[-1][:-1]
        res[-1]=int(res[-1])
        

        if res==['Request', 'failed', 'with', 'status', 'code', 404]: return False
        self.rank=res[0]
        if self.rank=='Radiant':
            self.rr=res[1]
            
            self.embed_rank=discord.Embed(
                color=var_tracky.colors[self.rank],
                title=f"**{self.pseudo}**#{self.tag}",
                description=f"**{self.rank} {self.rr}** RR"
            )

            self.file = discord.File("images/Radiant_Rank.png", filename="image.png")

            self.stats=(self.rank,self.rr)
        else:
            self.rank_num,self.rr=res[1:]
            # return self.rank,int(self.rank_num),self.rr
            self.embed_rank=discord.Embed(
                color=var_tracky.colors[self.rank],
                title=f"**{self.pseudo}**#{self.tag}",
                description=f"**{self.rank} {self.rank_num} {self.rr}** RR"
            )

            self.file = discord.File(f"images/{self.rank}_{self.rank_num}_Rank.png", filename="image.png")
            self.stats=(self.rank,self.rank_num,self.rr)
        

        return True

    
    def __eq__(self, joueur2) -> bool:
        Player1_stats=self.stats
        Player2_stats=joueur2.stats
        return Player1_stats==Player2_stats
    
   
        
    
    def __lt__(self, joueur2): #defini le <
        Player1_stats=self.stats
        Player2_stats=joueur2.stats
        
        # print(Player1_stats)
        # print(Playesr2_stats)
        
        rank1=Player1_stats[0]
        rank2=Player2_stats[0]
        
        
        
        if rank1==rank2=='Radiant':
            return Player1_stats[1]<Player1_stats[1]
        elif rank1=='Radiant':
            return False
        elif rank2=='Radiant':
            return True
        
        
        elif rank1==rank2:
            if Player1_stats[1]==Player2_stats[1]:
                return Player1_stats[2]<Player2_stats[2]
            else:
                return Player1_stats[1]<Player2_stats[1]
            
        else:
            return ranks.index(Player1_stats[0])<ranks.index(Player2_stats[0])
    
    
    
    
    
    def __gt__(self,joueur2): #defini le >
        return not((self<joueur2)or(self==joueur2))
        """
        Player1_stats=self.stats
        Player2_stats=joueur2.stats
        
        # print(Player1_stats)
        # print(Player2_stats)
        
        rank1=Player1_stats[0]
        rank2=Player2_stats[0]
        
        
        
        if rank1==rank2=='Radiant':
            return Player1_stats[1]>Player1_stats[1]
        elif rank1=='Radiant':
            return True
        elif rank2=='Radiant':
            return False
        
        
        elif rank1==rank2:
            if Player1_stats[0]==Player2_stats[0]:
                return Player1_stats[2]>Player2_stats[2]
            else:
                return int(Player1_stats[1])>int(Player2_stats[1])
            
        else:
            return ranks.index(Player1_stats[0])>ranks.index(Player2_stats[0])
        """

    def __le__(self, joueur2): #defini le <=
        return (self<joueur2) or (self==joueur2)
    
    def __ge__(self, joueur2): #defini le >=
        return (self>joueur2) or (self==joueur2)

# print(Joueur("Theophile","7023","eu"))
# print(Joueur("Theophile","7023","eu")<Joueur("Rayquax","NSFW","eu"))
# print(dir(Joueur))
# Theophile #7023