import unittest

from src.database import Database

class TestUserDatabase(unittest.IsolatedAsyncioTestCase):
    async def test_users_add(self):
        users = [
            ["1", "2", "3"],
            ["1", "2", "3"]
        ]
        for i in users:
            await Database.users.add(*i)

    async def test_users_get_all(self):
        users = await Database.users.get_all() 
        self.assertEqual(len(users) == 2, 2)

    async def test_users_get_by_id(self):
        user = await Database.users.find_by_id(0)
        self.assertNotEqual(user, None) 

    async def test_users_add_like():
        user = await Database.users.find_by_id()
        
        
        