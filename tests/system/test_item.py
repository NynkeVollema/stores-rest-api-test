from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()   # setUp overrules BaseTest setUp, so this needs to be called to have the app etc
        with self.app() as client:
            with self.app_context():
                UserModel("Test Username", "Test Password").save_to_db()
                auth_response = client.post("/auth",
                                            data=json.dumps({"username": "Test Username", "password": "Test Password"}),
                                            headers={"Content-Type": "application/json"})
                auth_token = json.loads(auth_response.data)["access_token"]  # this is our jwt token
                self.access_token = f"JWT " + auth_token    # string "JWT " needs to be included in token! (Flask JWT)

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/item/Test Item Name")   # without including authorisation header

                self.assertEqual(response.status_code, 401)     # 401 indicates missing authorisation header

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                # Next lines have been moved to setUp method! So we don't need to copy them in each test.
                # UserModel("Test Username", "Test Password").save_to_db()
                # auth_response = client.post("/auth",
                #                             data=json.dumps({"username": "Test Username", "password": "Test Password"}),
                #                             headers={"Content-Type": "application/json"})
                # auth_token = json.loads(auth_response.data)["access_token"]  # this is our jwt token
                # header = {"Authorization": "JWT " + auth_token}     # string "JWT " needs to be included! (Flask JWT)
                # # Alternatively, in Python 3.6, with string formatting:
                # # header = {"Authorization": f"JWT {auth_token}"}
                # response = client.get("/item/Test Item Name", headers=header)   # including authorisation header
                response = client.get("/item/Test Item Name", headers={"Authorization": self.access_token})   # including authorisation header

                self.assertEqual(response.status_code, 404)     # 401 indicates missing authorisation header

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                ItemModel("Test Item Name", 8.99, 1).save_to_db()
                response = client.get("/item/Test Item Name", headers={"Authorization": self.access_token})   # including authorisation header

                self.assertEqual(response.status_code, 200)

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                ItemModel("Test Item Name", 8.99, 1).save_to_db()
                response = client.delete("/item/Test Item Name")  # only get method needs authorisation header

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"message": "Item deleted."},
                                     json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                response = client.post("/item/Test Item Name", data={"price": 17.99, "store_id": 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({"name": "Test Item Name", "price": 17.99},
                                     json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                ItemModel("Test Item Name", 17.99, 1).save_to_db()
                # Alternatively:
                # client.post("/item/Test Item Name", data={"price": 17.99, "store_id": 1})
                response = client.post("/item/Test Item Name", data={"price": 17.99, "store_id": 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "An item with name 'Test Item Name' already exists."},
                                     json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                response = client.put("/item/Test Item Name", data={"price": 17.99, "store_id": 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name("Test Item Name").price, 17.99)
                self.assertDictEqual({"name": "Test Item Name", "price": 17.99},
                                     json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                ItemModel("Test Item Name", 8.99, 1).save_to_db()

                self.assertEqual(ItemModel.find_by_name("Test Item Name").price, 8.99)

                response = client.put("/item/Test Item Name", data={"price": 17.99, "store_id": 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name("Test Item Name").price, 17.99)
                self.assertDictEqual({"name": "Test Item Name", "price": 17.99},
                                     json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                ItemModel("Test Item Name", 8.99, 1).save_to_db()
                response = client.get("/items")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"items": [{"name": "Test Item Name", "price": 8.99}]},
                                     json.loads(response.data))
