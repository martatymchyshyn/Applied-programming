import unittest
import sqlalchemy
from main import app
from base64 import b64encode
import json
from modules import engine

class TestingBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    tester = app.test_client()
    creds = b64encode(b"nogami:neuro").decode("utf-8")


class UserApiTest(TestingBase):
    data = {
        "first_name": "Marta",
        "last_name": "Tymchyshyn",
        "password": "qwerty",
        "user_name": "nogami"
    }

    def test_UserCreation(self):
        delete()
        response = self.tester.post("/api/v1/users", data=json.dumps(self.data), content_type="application/json")
        code = response.status_code
        self.assertEqual(201, code)

    def test_UserCreation_with_exist_username(self):
        delete()
        insertuser()
        response = self.tester.post("/api/v1/users", data=json.dumps(self.data), content_type="application/json")
        code = response.status_code
        self.assertEqual(400, code)

    def test_InvalidUserCreation(self):
        delete()
        response = self.tester.post("/api/v1/users", data=json.dumps({"user_name": 1}), content_type="application/json")
        code = response.status_code
        self.assertEqual(400, code)

    def test_get_user_by_id(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/users/me', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)


    def test_unauthorized(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/users/me', headers={"Authorization": "Basic lol:keke"})
        code = response.status_code
        self.assertEqual(401, code)

    def test_UpdateUser(self):
        delete()
        insertuser()
        response = self.tester.put('/api/v1/users', data=json.dumps({"first_name": "lolo", "last_name": "lolo2", "password": "qwertyu"}),content_type='application/json',  headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_GetAllUsers(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/users')
        code = response.status_code
        self.assertEqual(200, code)

    def test_DeleteUser(self):
        delete()
        insertuser()
        response = self.tester.delete('/api/v1/users', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)






class Locations(TestingBase):
    location_data = {
        "name": "Lviv"
    }

    def test_location_creation(self):
        delete()
        insert_user_without_location()
        response = self.tester.post('/api/v1/locations',
                                    data=json.dumps(self.location_data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(201, code)

class TestAds(TestingBase):

    ad_data = {
        "title": "lolo",
        "body": "lolololo"
    }
    bad_ad_data = {
        "title": "lolo",
        "body": "lolololo"
    }
    def test_Creation_Advertisement(self):
        delete()
        insertuser()
        response = self.tester.post('/api/v1/ads',
                                    data = json.dumps(self.ad_data),
                                    content_type = 'application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(201, code)

    def test_get_all_ads(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/ads', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_delete_ad(self):
        delete()
        insertuser()
        insertads()
        response = self.tester.delete('/api/v1/ads/1', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_delete_unexisting_ad(self):
        delete()
        insertuser()
        response = self.tester.delete('/api/v1/ads/1', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_fetch_public_ads(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/ads/public')
        code = response.status_code
        self.assertEqual(200, code)

    def test_fetch_my_ads(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/ads/my', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_create_invalid_ad(self):
        delete()
        insert_user_without_location()
        response = self.tester.post('/api/v1/ads',
                                    data = json.dumps(self.ad_data),
                                    content_type = 'application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(400, code)
def delete():
    file = open("C:\\Users\\Marta\\Desktop\\LABA4\\clean.sql")
    clean = sqlalchemy.text(file.read())
    engine.execute(clean)
    file.close()
def insertuser():
    insert_file = open("C:\\Users\\Marta\\Desktop\\LABA4\\insert.sql")
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()
def insertads():
    insert_file = open('C:\\Users\\Marta\\Desktop\\LABA4\\insertads.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()
def insert_user_without_location():
    insert_file = open('C:\\Users\\Marta\\Desktop\\LABA4\\insertuserwithoutlocation.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()


if __name__ == '__main__':
    unittest.main()