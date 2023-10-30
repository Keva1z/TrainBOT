from database.models import Reward, User, Unit
from bot.console_log import logger
import aiosqlite
import asyncio
import os

DB_PATH = os.getenv("DB_PATH")

class database():   
    @staticmethod
    def load() -> None:
        async def create_tables() -> None:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('CREATE TABLE IF NOT EXISTS USER_DATA'
                                '(TELEGRAM_ID INTEGER PRIMARY KEY, DATA BLOB)')
                await db.execute('CREATE TABLE IF NOT EXISTS REWARD_DATA'
                                '(TELEGRAM_ID INTEGER PRIMARY KEY, DATA BLOB)')

                await db.commit()
            logger.database.log("Database tables created successfully")
            
        asyncio.run(create_tables())
    
    class user():
        @staticmethod
        async def get_ids():
            async with aiosqlite.connect(DB_PATH) as db:
                async with db.execute('SELECT TELEGRAM_ID FROM USER_DATA') as cursor:
                    return [i[0] for i in await cursor.fetchall()]
        
        @staticmethod
        async def load(id: int) -> User.USER:
            user = await User.USER(id).get_data()
            rewards = await database.reward.load(id)
            user.rewards = rewards.rewards
            return user
        
        @staticmethod
        async def save(user: User.USER | list[User.USER]) -> None:
            if type(user) == list:
                for i in user:
                    await i.save_data()
            else:
                await user.save_data()
            
        @staticmethod
        async def new(id:int, name: str | None = None, username: str | None = None) -> User.USER:
            logger.database.log(f"User '{id}' created successfully")
            return await User.USER(id).new(name, username)
        
    class reward():
        @staticmethod
        async def add(name: str, reward_list: Reward.REWARD) -> None:
            reward_list.rewards.append(Unit.UNIT(name))
            await database.reward.save(reward_list)
        
        @staticmethod
        async def load(id: int) -> Reward.REWARD:
            return await Reward.REWARD(id).get_data()
        
        @staticmethod
        async def save(reward: Reward.REWARD) -> None:
            await reward.save_data()
            
        @staticmethod
        async def new(id:int) -> Reward.REWARD:
            logger.database.log(f"User '{id}' rewards created successfully")
            return await Reward.REWARD(id).new()