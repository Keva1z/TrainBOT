import sys
sys.path.extend("../database")

from database.encoding.RSA_system import encrypt, decrypt
import aiosqlite
import os

DB_PATH = os.getenv("DB_PATH")
class REWARD():
        
    def __init__(self, id: int) -> None:
        self.telegram_id = id
        self.rewards = None
        
    async def new(self) -> None:
        self.rewards = []
        return await self.save_data()
        
    
    def create_data(self):
        return {
            'rewards' : self.rewards,
        }
        
    async def parse_data(self, data):
        self.rewards = data['rewards']
    
    async def save_data(self) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(f'SELECT DATA FROM REWARD_DATA WHERE TELEGRAM_ID =?', (self.telegram_id,)) as cursor:
                data = await cursor.fetchone()
                if data is None:
                    await db.execute(f'INSERT INTO REWARD_DATA (TELEGRAM_ID, DATA) VALUES (?,?)',
                                     (self.telegram_id, await encrypt(self.create_data())))
                else:
                    await db.execute(f'UPDATE REWARD_DATA SET DATA =? WHERE TELEGRAM_ID =?',
                                     (await encrypt(self.create_data()), self.telegram_id))
            await db.commit()
        return self
                    
    async def get_data(self) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.cursor() as cursor:
                await cursor.execute(f'SELECT DATA FROM REWARD_DATA WHERE TELEGRAM_ID =?', (self.telegram_id,))
                data = await cursor.fetchone()
                if data is None:
                    await self.new()
                else:
                    await self.parse_data(await decrypt(data[0]))            
                await db.commit()
        return self