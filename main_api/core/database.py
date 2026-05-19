from sqlite3 import connect
from aiosqlite import connect as connect2

class ManageDB:
    def __init__(self, db_name):
        self.db_name = db_name
        with connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS pins(id INTEGER, name TEXT, value INTEGER)')

    async def exec(self, query, p=None, fetch_one=False, fetch_all=False):
        async with connect2(self.db_name) as db:
            cursor  = await db.execute(query, p)
            if fetch_one:
                return await cursor.fetchone()
            if fetch_all:
                return await cursor.fetchall()
            await db.commit()

    async def addPin(self, gpio, name):
        await self.exec('INSERT INTO pins VALUES (?, ?, 0)', (gpio, name, ))
        return True

    async def delPin(self, gpio):
        if int(gpio) in (await self.GetAllPins()):
            await self.exec('DELETE FROM pins WHERE id = ?', (gpio,))
            return True
        return False
    
    async def GetAllPins(self):
        return dict(await self.exec('SELECT id, value FROM pins', fetch_all=True))
    
    async def GetAllPins2(self):
        return await self.exec('SELECT * FROM pins', fetch_all=True)

    async def ChangeValue(self, gpio, value = None):
        pins = await self.GetAllPins()
        if gpio not in pins:
            return False
        if value is None:
            value = not pins[gpio]
        await self.exec('UPDATE pins SET value = ? WHERE id = ?', (value, gpio,))
        return True