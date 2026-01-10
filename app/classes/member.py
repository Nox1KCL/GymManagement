from .user import User


class Member(User):
    def __init__(self, name, password, workouts, status, access):
        super().__init__(name, password)
        self.workouts = workouts
        self.status = status
        self.access = access


    def gather_info(self) -> dict:
        user_data = {
            "workouts": self.workouts,
            "status": self.status,
            "access": self.access,
            "password": self.password
        }
        return user_data


    def __str__(self):
        return f"Name: {self.name}, count of workouts: {self.workouts}, status: {self.status}"