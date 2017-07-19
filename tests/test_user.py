import unittest

from classes.users import Users

class Test_user(unittest.TestCase):
    """
    tests for registration and login for user accounts

    """
    def setUp(self):
        self.users = Users()

    def test_name(self):
        self.assertEqual(self.users.register(1332, "email@mail.com", "password"), 
            "Name cannot contain numbers")
    
    def test_password(self):
        self.assertEqual(self.users.register('name', "email@mail.com", " "), 
            "Password length should be at least 6 characters")
        self.assertEqual(self.users.register('name', "email@mail.com", "1234"), 
            'Password length should be at least 6 characters')

    def test_registration_successfull(self):
        self.users.register("Dennis", "example@test.com", "password")
        user_account = {"example@test.com":{'name': "Dennis", "password":"password"}}
        self.assertEqual(self.users.users, user_account)

    def test_duplicate_name(self):
        self.users.register("myname", "email@mail.com", "password")
        self.assertEqual(self.users.register("myname", "email@mail.com", "password"), 
            'Email already exists.')

    def test_login(self):
        self.assertEqual(self.users.login("", "password"), 
            "email field cannot be left empty")
        self.assertEqual(self.users.login("email@mail.com", " "), 
            "User does not exist.")

    def test_check_user_exists(self):
        self.assertEqual(self.users.login("unknown_email", "password"), 
            "User does not exist.")
    
    def test_wrong_password(self):
        #create an account
        self.users.register("name", "email@gmail.com", "password")

        #login with the correct email and wrong password
        self.assertEqual(self.users.login("email@gmail.com", "passward"), 
            "Incorect password")
    
    def test_logout(self):
        self.users.logout()
        self.assertTrue(self.users.user_is_logged_in is None)
    
    def test_user_logs_in(self):
        self.assertTrue(self.users.login("email@gmail.com", "password"))
    
         