import asyncio,aiohttp


aiohttp.client.ClientSession.post



async def req(session):
    async with session.get('https://api.kyroskoh.xyz/valorant/v1/mmr/eu/Rayquax/NSFW?show=combo&display=0') as resp:
        try: resp=await resp.read()
        except: raise
        
        return resp
    
    
async def force():
    async with aiohttp.ClientSession() as session:
    
        
        a=await req(session)
        print(a.decode())

asyncio.run(force())