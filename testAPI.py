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

    def test_User_Creation(self):
        delete()
        response = self.tester.post("/api/v1/users", data=json.dumps(self.data), content_type="application/json")
        code = response.status_code
        self.assertEqual(201, code)

    def test_User_Creation_With_Exist_Username(self):
        delete()
        insertuser()
        response = self.tester.post("/api/v1/users", data=json.dumps(self.data), content_type="application/json")
        code = response.status_code
        self.assertEqual(400, code)

    def test_Invalid_User_Creation(self):
        delete()
        response = self.tester.post("/api/v1/users", data=json.dumps({"user_name": 1}), content_type="application/json")
        code = response.status_code
        self.assertEqual(400, code)

    def test_Get_User_By_Id(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/users/me', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Unauthorized(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/users/me', headers={"Authorization": "Basic authorization eror"})
        code = response.status_code
        self.assertEqual(401, code)

    def test_Update_User(self):
        delete()
        insertuser()
        response = self.tester.put('/api/v1/users',
                                   data=json.dumps({"first_name": "lolo", "last_name": "lolo2", "password": "qwertyu"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Get_All_Users(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/users')
        code = response.status_code
        self.assertEqual(200, code)

    def test_Delete_User(self):
        delete()
        insertuser()
        response = self.tester.delete('/api/v1/users', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)


class Locations_Tests(TestingBase):
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


class Test_For_Advertisements(TestingBase):
    advertisements_data = {
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
                                    data=json.dumps(self.advertisements_data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(201, code)

    def test_Get_All_Advertisements(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/ads', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Delete_Advertisement(self):
        delete()
        insertuser()
        insertads()
        response = self.tester.delete('/api/v1/ads/1', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Delete_Unexisting_Advertisement(self):
        delete()
        insertuser()
        response = self.tester.delete('/api/v1/ads/1', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_Fetch_Public_Advertisements(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/ads/public')
        code = response.status_code
        self.assertEqual(200, code)

    def test_Fetch_My_Advertisements(self):
        delete()
        insertuser()
        response = self.tester.get('/api/v1/ads/my', headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_Create_Invalid_Advertisement(self):
        delete()
        insert_user_without_location()
        response = self.tester.post('/api/v1/ads',
                                    data=json.dumps(self.advertisements_data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(400, code)


# method to delete from database
def delete():
    file = open("C:\\Users\\Marta\\Desktop\\LABA4\\clean.sql")
    clean = sqlalchemy.text(file.read())
    engine.execute(clean)
    file.close()


# method to add user
def insertuser():
    insert_file = open("C:\\Users\\Marta\\Desktop\\LABA4\\insert.sql")
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()


# method to add an advertisement
def insertads():
    insert_file = open('C:\\Users\\Marta\\Desktop\\LABA4\\insertads.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()


# method to add user without location
def insert_user_without_location():
    insert_file = open('C:\\Users\\Marta\\Desktop\\LABA4\\insertuserwithoutlocation.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()


if __name__ == '__main__':
    unittest.main()
