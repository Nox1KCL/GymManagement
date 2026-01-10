from .user import User


class Admin(User):
    def __init__(self, name, password, access):
        super().__init__(name, password)
        self.access = access
    
    
    def gather_info(self) -> dict:
        admin_data = {
            "password": self.password,
            "access": self.access
        }
        return admin_data


    def __str__(self):
        return f"Name: {self.name}, access: {self.access}"