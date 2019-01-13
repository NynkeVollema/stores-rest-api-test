from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel("Test Store Name").save_to_db()  # necessary for other platforms than sqlite
            item = ItemModel("Test Item Name", 8.99, 1)

            self.assertIsNone(ItemModel.find_by_name("Test Item Name"),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name("Test Item Name"))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name("Test Item Name"))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test Store Name")
            item = ItemModel("Test Item Name", 8.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, "Test Store Name")