from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/Test Store Name")

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("Test Store Name"))
                self.assertDictEqual({"id": 1, "name": "Test Store Name", "items": []},
                                     json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store Name")
                response = client.post("/store/Test Store Name")

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A store with name 'Test Store Name' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store Name")
                # Alternatively:
                # StoreModel("Test Store Name").save_to_db()
                response = client.delete("/store/Test Store Name")  # can be GET, POST, DELETE, PUT, PATCH, etc

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"message": "Store deleted."},
                                     json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/Test Store Name")
                response = client.get("/store/Test Store Name")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"id": 1, "name": "Test Store Name", "items": []},
                                     json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/Test Store Name")

                self.assertEqual(response.status_code, 404) # 404 means "not found", so next test might be left out
                self.assertDictEqual({"message": "Store not found."},
                                     json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                # Alternatively:
                # client.post("/store/Test Store Name")
                ItemModel("Test Item Name", 8.99, 1).save_to_db()
                response = client.get("/store/Test Store Name")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"id": 1, "name": "Test Store Name", "items": [{"name": "Test Item Name", "price": 8.99}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                response = client.get("/stores")

                self.assertDictEqual({"stores": [{"id": 1, "name": "Test Store Name", "items": []}]},
                                     json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("Test Store Name").save_to_db()
                ItemModel("Test Item Name", 8.99, 1).save_to_db()
                response = client.get("/stores")

                self.assertDictEqual({"stores": [{"id": 1, "name": "Test Store Name", "items": [{"name": "Test Item Name", "price": 8.99}]}]},
                                     json.loads(response.data))
