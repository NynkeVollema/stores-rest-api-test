from models.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel("Test Item Name", 8.99, 1)

        self.assertEqual(item.name, "Test Item Name",
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 8.99,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.store_id, 1,
                         "The store id of the item after creation does not equal the constructor argument.")
        self.assertIsNone(item.store)

    def test_item_json(self):
        item = ItemModel("Test Item Name", 8.99, 1)
        expected = {
            "name": "Test Item Name",
            "price": 8.99
        }

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(), expected))
