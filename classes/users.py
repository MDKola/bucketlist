class Users(object):

    def __init__(self):
        self.users = {}
        self.user_is_logged_in = None
    
    def register(self, name, email, password):
        error_msg = None

        if type(name) != str:
            error_msg = "Name cannot contain numbers"

        if len(password) < 6:
            error_msg = 'Password length should be at least 6 characters'

        if len(email) < 0:
            error_msg = 'Please provide an email address.'

        if error_msg is None:
            user_exists = False
            for reg_email in self.users.keys():
                if email == reg_email:
                    user_exists = True
                    error_msg = 'Email already exists.'
                    break

            if not user_exists:
                #create account
                self.users[email] = {'password': password, 'name': name}

        if error_msg is not None:
            return error_msg
    
    def login(self, email, password):
        error_msg = None

        if len(password) == 0:
            error_msg = 'Invalid password'

        elif len(email) == 0:
            error_msg = 'email field cannot be left empty'
        
        if error_msg is None:
            user_in_record = False
            for reg_email in self.users.keys():
                if email == reg_email:
                    user_in_record = True
                    reg_user_details = self.users[email]
                    reg_password = reg_user_details['password']

                    if password == reg_password:
                        self.user_is_logged_in = email
                    else:
                        error_msg = 'Incorect password'
                    break

            if not user_in_record:
                error_msg = 'User does not exist.'
                
        if error_msg is not None:
            return error_msg
    
    def logout(self):
        self.user_is_logged_in = None