import sys
sys.path.extend("../database")

from database.encoding.RSA_system import encrypt, decrypt
import aiosqlite
import os

DB_PATH = os.getenv("DB_PATH")

class USER():
    def __init__(self, id: int) -> None:
        self.telegram_id = id
        self.name = None
        self.username = None
        self.userid = None
        self.sex = None
        self.completed = None
        self.completed_today = None
        self.current_weight = None
        self.start_weight = None
        self.task_list = None
        self.partner_id = None
        self.plans = None
        self.current_plan = None
        self.active = None
        self.active_message = None
        self.rewards = None
        
    async def new(self, name: str | None, username: str | None) -> None:
        self.name = name
        self.username = username
        self.userid = self.telegram_id
        self.sex = "MALE"
        self.completed = 0
        self.completed_today = 0
        self.current_weight = 0
        self.start_weight = 0
        self.task_list = []
        self.partner_id = None
        self.plans = {}
        self.current_plan = None
        self.active = False
        self.active_message = None
        return await self.save_data()
        
    
    def create_data(self):
        return {
            'name': self.name,
            'username': self.username,
            'userid': self.userid,
            'sex': self.sex,
            'completed': self.completed,
            'completed_today' : self.completed_today,
            'current_weight': self.current_weight,
            'start_weight': self.start_weight,
            'task_list': self.task_list,
            'partner_id': self.partner_id,
            'plans': self.plans,
            'current_plan': self.current_plan,
            'active' : self.active,
            'active_message' : self.active_message
        }
        
    async def parse_data(self, data):
        self.name = data['name']
        self.username = data['username']
        self.userid = data['userid']
        self.sex = data['sex']
        self.completed = data['completed']
        self.completed_today = data['completed_today']
        self.current_weight = data['current_weight']
        self.start_weight = data['start_weight']
        self.task_list = data['task_list']
        self.partner_id = data['partner_id']
        self.plans = data['plans']
        self.current_plan = data['current_plan']
        self.active = data['active']
        self.active_message = data['active_message']
    
    async def save_data(self) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(f'SELECT DATA FROM USER_DATA WHERE TELEGRAM_ID =?', (self.telegram_id,)) as cursor:
                data = await cursor.fetchone()
                if data is None:
                    await db.execute(f'INSERT INTO USER_DATA (TELEGRAM_ID, DATA) VALUES (?,?)',
                                     (self.userid, await encrypt(self.create_data())))
                else:
                    await db.execute(f'UPDATE USER_DATA SET DATA =? WHERE TELEGRAM_ID =?',
                                     (await encrypt(self.create_data()), self.userid))
            await db.commit()
        return self
                    
    async def get_data(self) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.cursor() as cursor:
                await cursor.execute(f'SELECT DATA FROM USER_DATA WHERE TELEGRAM_ID =?', (self.telegram_id,))
                data = await cursor.fetchone()
                if data is None:
                    await self.new(None, None)
                else:
                    await self.parse_data(await decrypt(data[0]))            
                await db.commit()
        return self
        