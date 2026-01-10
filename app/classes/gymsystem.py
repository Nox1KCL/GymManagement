from classes.member import Member
from utils import logging, get_mac_address, hash_password
import json
from pathlib import Path


class System:   
    def __init__(self, f_path: Path):
        self.f_path = f_path
        self.__gym_data = self.load_from_file()

    
    @property
    def gym_data(self) -> dict:
        return self.__gym_data


    def sign_up(self, category: str, login: str, password: str, workouts: int) -> None:
        hashed_pass = hash_password(password)
        member = Member(login, hashed_pass, workouts, "good", "low")
        member_data = member.gather_info()

        self.gym_data[category]['logins'][member.name] = member_data
        logging.info(f'| {login} | is registered')
        self.save_to_json(self.gym_data)
        

    def sign_in(self, category: str, login: str, password: str) -> None:
        logging.info(f"Login attempt from {get_mac_address}")
        input_hash = hash_password(password)

        if login in self.gym_data[category]['logins']:
            stored_hash = self.gym_data[category]['logins'][login]['password']
            if input_hash == stored_hash:
                # print(f"User: {login}")
                for key, value in self.gym_data[category]['logins'][login].items():
                    if key == "password":
                        continue
                    print(f"{key}: {value}")
                # print()
                # print("You are logged in.")
                logging.info(f"User: | {login} | logged")
                # TODO Management func
            else:
                # print("Nickname or Password is incorrect")
                logging.info("Nickname or Password is incorrect")
        else:
            # print("Nickname or Password is incorrect")
            logging.info("Nickname or Password is incorrect")


    def entrance(self) -> None:
        whats_user = int(input("1 - Member\n"
                "2 - Admin\n"
                "Your option: "))

        choice = int(input("1 - Sign-up\n"
                "2 - Sign-in\n"
                "Your option: "))

        match whats_user:
            case 1:
                category = 'members'

                if choice == 1:
                    name = input("Write your name(3-10 letters): ")
                    password = input("Input your password(6-24 letters): ")
                    workouts = int(input("Enter the number of workouts you need(1-10): "))
                    self.sign_up(category, name, password, workouts)

                else:
                    login = input("Input your login: ")
                    password = input("Enter password: ")
                    print()
                    self.sign_in(category, login, password)

            case 2:
                category = 'admins'

                if choice == 1:
                    print("Ask to Headmaster for add you as admin")

                else:
                    login = input("Input your login: ")
                    password = input("Enter password: ")
                    print()
                    self.sign_in(category, login, password)


    def load_from_file(self) -> dict:
        default_data = {
            'members': {
                'logins': {}
            }, 
            'admins': {
                'logins': {}
            }
        }
        try:
            with open(self.f_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError as e:
            logging.info(f"Error: {e}")
            data = default_data

        return data

    
    def save_to_json(self, data: dict) -> None:
        with open(self.f_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"File saved to {self.f_path}")