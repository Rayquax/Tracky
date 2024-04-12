
import json,time,aiohttp,asyncio


words=open("wordlist.txt","r").read().split("\n")

class Mot:
    def __init__(self,name: str, score: float) -> None:
        self.score=score
        self.name=name
    def __lt__(self, other):
        return self.score<other.score
    def __gt__(self, other):
        return self.score>other.score
    def __le__(self, other):
        return self.score<=other.score
    def __ge__(self, other):
        return self.score>=other.score
    def __eq__(self, other):
        return self.score==other.score
    def __repr__(self) -> str:
        return self.name+" : "+str(self.score)

url = 'https://cemantix.certitudes.org/score'

headers = json.loads(open("headers.json").read())


async def req(word,session):
    data = {"word": word}
    async with session.post('/score',data=data,headers=headers) as resp:
        try: resp=await resp.json()
        except: exit()
        
        return Mot(word, resp['score']) if 'score' in resp.keys() else Mot(word, -100)
        
async def get_scores(session, batch):
    tasks=[req(word,session) for word in batch]
    return await asyncio.gather(*tasks)

async def force():
    async with aiohttp.ClientSession('https://cemantix.certitudes.org/') as session:
        
        a=await get_scores(session,words)
        a.sort()
        print(max(a))


start=time.time()
asyncio.run(force())
print(time.time()-start)
        


