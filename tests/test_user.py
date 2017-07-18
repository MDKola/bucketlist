import unittest

from classes.users import Users

class Test_user(Unittest.TestCase):
    """
    tests for registration and login for user accounts

    """
    def setUp(self):
        self.users = Users()

    def test_name(self):
        self.assertEqual(self.users.register(" ", "password"), "Name field cannot be left empty")
        self.assertEqual(self.users.register('1332d', "password"), "Name cannot contain numbers")
    
    def test_password(self):
        self.assertEqual(self.users.register('name', " "), "password field cannot be empty")
        self.assertEqual(self.users.register('name', "1234"), 'Password length should be at least 6 characters')

    def test_registration successfull(self):
        self.users.register("Denis", "example@test.com", "password")
         