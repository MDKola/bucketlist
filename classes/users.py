class Users(object):
    def __init__(self):
        self.users = {}
        self.user_is_logged_in = False
    
    def register(self, name, email, password):
        msg = None
        user_exists = False
        for registered_email in self.users.keys():
            if email == registered_email:
                user_exists = True
                msg = "An email {} already exists.".format(str(email))
                break
        if not user_exists:
            self.users[email] = {'name': name, 'password': password}

        if msg is not None:
            return msg
    
    def login(self, email, password ):
        if registered_email in self.users.keys():
            if email == registered_email:
                registered_user = self.users[email]
                registered_password = registered_user['password']
                if password == registered_password:
                    self.user_is_logged_in = email
                else:
                    msg = "Invalid password"

                break 

