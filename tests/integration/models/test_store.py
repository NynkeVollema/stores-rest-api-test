from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("Test Store Name")

        self.assertListEqual(store.items.all(), [],
                             "The store's items length was not 0 even though no items were added.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel("Test Store Name")

            self.assertIsNone(StoreModel.find_by_name("Test Store Name"),
                              "Found a store with name {}, but expected not to.".format(store.name))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name("Test Store Name"))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name("Test Store Name"))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test Store Name")
            item = ItemModel("Test Item Name", 8.99, 1)     # store_id needs to be 1 (it is the first store created)

            store.save_to_db()  # save store first: store doesn't need item, but item does need store!
            item.save_to_db()   # store needs to exist before item can be created!

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, "Test Item Name")

    def test_store_json(self):
        store = StoreModel("Test Store Name")
        expected = {
            "id": None,     # id will always be None before we save the store to the database
            "name": "Test Store Name",
            "items": []
        }

        self.assertDictEqual(store.json(), expected,
            "The JSON export of the store is incorrect. Received {}, expected {}.".format(store.json(), expected))

    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel("Test Store Name")
            item = ItemModel("Test Item Name", 8.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                "id": 1,
                "name": "Test Store Name",
                "items": [{"name": "Test Item Name", "price": 8.99}]
            }

            self.assertDictEqual(store.json(), expected,
                "The JSON export of the store is incorrect. Received {}, expected {}.".format(store.json(), expected))
