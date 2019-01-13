from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("Test Username", "Test Password")

        self.assertEqual(user.username, "Test Username",
                         "The username after creation does not equal the constructor argument.")
        self.assertEqual(user.password, "Test Password",
                         "The password after creation does not equal the constructor argument.")
