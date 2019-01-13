"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):    # Runs once for each test case
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config["DEBUG"] = False     # explained in last 2 minutes of Lecture 79
        app.config["PROPAGATE_EXCEPTIONS"] = True   # explained in last 2 minutes of Lecture 79
        # Make sure database exists
        with app.app_context():
            db.init_app(app)

    def setUp(self):        # Runs once for every test method (e.g. within a test class)
        with app.app_context():
            db.create_all()
        # Get a test client
        # self.app = app.test_client()       # Creates a test client that is reused in every test
        self.app = app.test_client          # Creates a new test client for every test
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
