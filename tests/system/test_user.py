from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:      # This allows for post requests etc to be done to the api.
            with self.app_context():    # This is needed because the register method needs a database.
                response = client.post("/register", data={"username": "Test Username", "password": "Test Password"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("Test Username"))
                self.assertDictEqual({"message": "User was created successfully."},
                                     json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                # /register accepts data in form format, /auth only accepts data in json format
                # A header is just another piece of data that can go in a request.
                # The Content-Type header is used to tell a web server what type of data you're sending it.
                client.post("/register", data={"username": "Test Username", "password": "Test Password"})
                auth_response = client.post("/auth",
                                           data=json.dumps({"username": "Test Username", "password": "Test Password"}),
                                           headers={"Content-Type": "application/json"})

                self.assertIn("access_token", json.loads(auth_response.data).keys())     # ["access_token"]

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                # Instead of using the post, you can also just create a UserModel object and save it to the database.
                client.post("/register", data={"username": "Test Username", "password": "Test Password"})
                response = client.post("/register", data={"username": "Test Username", "password": "Test Password"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A user with that username already exists."},
                                     json.loads(response.data))
