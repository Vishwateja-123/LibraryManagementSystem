class User:
    def __init__(self, userId, name, username, password):
        self.userId = userId
        self.name = name
        self.username = username
        self.password = password
        self.loggedIn = False

    def login(self, username, password):
        if self.username == username and self.password == password:
            self.loggedIn = True
            return True

        return False

    def logout(self):
        self.loggedIn = False
        return True
