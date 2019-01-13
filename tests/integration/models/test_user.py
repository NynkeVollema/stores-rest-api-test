from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel("Test Username", "Test Password")

            self.assertIsNone(UserModel.find_by_username("Test Username"),
                              "Found a user with name {}, but expected not to.".format(user.username))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            # These two lines also test the find_by_name and find_by_id functions!
            # So, no separate tests are necessary for that.
            self.assertIsNotNone(UserModel.find_by_username("Test Username"))
            self.assertIsNotNone(UserModel.find_by_id(1))
