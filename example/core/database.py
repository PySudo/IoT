from sqlite3 import connect
from aiosqlite import connect as connect2

def flatten(lst):
    out = list()
    for i in lst:
        try:
            out.extend(i)
        except:
            out.append(i)
    return out

class ManageDB:
    def __init__(self, db_name):
        self.db_name = db_name
        with connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS admins(id INTEGER, step TEXT, mess INTEGER)')

    async def exec(self, query, p=None, fetch_one=False, fetch_all=False):
        async with connect2(self.db_name) as db:
            cursor  = await db.execute(query, p)
            if fetch_one:
                return await cursor.fetchone()
            if fetch_all:
                return await cursor.fetchall()
            await db.commit()

    async def addAdmin(self, id):
        await self.exec('INSERT INTO admins VALUES (?, \'home\', 0)', (id,))
        return True

    async def delAdmin(self, id):
        if int(id) in (await self.GetAllAdmins()):
            await self.exec('DELETE FROM admins WHERE id = ?', (id,))
            return True
        return False

    async def GetAllAdmins(self):
        return flatten(await self.exec('SELECT id FROM admins', fetch_all=True))
    
    async def SetStep(self, id, step):
        await self.exec('UPDATE admins SET step = ? WHERE id = ?', (step, id,))

    async def SetMessageID(self, id, message_id):
        await self.exec('UPDATE admins SET mess = ? WHERE id = ?', (message_id, id,))
    
    async def GetStep(self, id):
        res = (await self.exec('SELECT step FROM admins WHERE id = ?', (id,), True))
        if res:
            return res[0]
        return 'home'
    
    async def GetMEssageID(self, id):
        res = (await self.exec('SELECT mess FROM admins WHERE id = ?', (id,), True))
        if res:
            return res[0]
        return 0