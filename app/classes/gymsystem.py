# region Imports

from typing import Generator
from classes.member import Member
from utils import logging, get_mac_address, hash_password, clear_console
import json
from pathlib import Path
from typing import Generator

# endregion


class System:
    def __init__(self, f_path: Path):
        self.f_path = f_path
        self.__gym_data = self.load_from_file()

    
    @property
    def gym_data(self) -> dict:
        return self.__gym_data


    def entrance(self) -> None:
        while True:
            try:

                whats_user = int(input("1 - Member\n"
                        "2 - Admin\n"
                        "Your option: "))
                
                choice = int(input("1 - Sign-up\n"
                        "2 - Sign-in\n"
                        "Your option: "))

                break
            except ValueError:
                clear_console()
                print('Enter correct option')

        clear_console()
        match whats_user:
            case 1:
                category = 'members'

                if choice == 1:
                    while True:
                        try:

                            name = input("Write your name(3-10 letters): ")
                            if len(name) < 3 or len(name) > 10:
                                print("Len of your name is not valid")
                            password = input("Input your password(6-24 letters): ")
                            if len(password) < 6 or len(password) > 24:
                                print("Your password is so short or so long")
                            workouts = int(input("Enter the number of workouts(1-10): "))
                            if workouts < 1 or workouts > 10:
                                print("Not acceptable number of workouts")

                            break
                        except ValueError:
                            clear_console()
                            print("Enter a number")

                    self.sign_up(category, name, password, workouts)

                else:
                    login = input("Input your login: ")
                    password = input("Enter password: ")
                    self.sign_in(category, login, password)

            case 2:
                category = 'admins'

                if choice == 1:
                    print("Ask to Headmaster for add you as admin")

                else:
                    login = input("Input your login: ")
                    password = input("Enter password: ")
                    self.sign_in(category, login, password)
            
            case _:
                print("Not valid command")


    def sign_up(self, category: str, login: str, password: str, workouts: int) -> None:
        hashed_pass = hash_password(password)
        member = Member(login, hashed_pass, workouts, "good", "low")
        member_data = member.gather_info()

        self.gym_data[category]['logins'][member.name] = member_data
        logging.info(f'| {login} | is registered')
        self.save_to_json(self.gym_data)
        

    def sign_in(self, category: str, login: str, password: str) -> None:
        clear_console()
        whoisthis = f"{category.upper()[:-1]}"
        logging.info(f"Login attempt from {get_mac_address()} | {whoisthis}")
        input_hash = hash_password(password)

        if login in self.gym_data[category]['logins']:
            stored_hash = self.gym_data[category]['logins'][login]['password']
            if input_hash == stored_hash:
                print(f"User: {login}")
                for key, value in self.gym_data[category]['logins'][login].items():
                    if key == "password":
                        continue
                    print(f"{key}: {value}")
                print("You are logged in.")
                logging.info(f"User: | {login} | logged")
                self.admin_panel()
            else:
                print("Nickname or Password is incorrect")
        else:
            print("Nickname or Password is incorrect")


    def admin_panel(self) -> None:
        print("-" * 10)
        print("Admin panel")
        print("-" * 10)
        while True:
            try:

                choice = int(input("1 - User management\n"
                            "2 - exit\n"
                            "Your option: "))

                break
            except ValueError:
                print("Enter the number")

        match choice:
            case 1:
                self.choose_user()
            case 2:
                print("Finishing work..")
                return

    
    def choose_user(self) -> None:
            gen = self.browse_users()
            deleg = self.delegator(gen)
            for user_login, user_data in deleg:
                choice = input("p(pick) or n(next): ")
                match choice.lower():
                    case 'p' | 'pick':
                        self.user_management(user_login, user_data)
                    case 'n' | 'next':
                        pass
                    case _:
                        print("Unknown command")
                        break

    
    def browse_users(self) -> Generator[tuple[str, dict], None, str]:
        clear_console()
        for user in self.gym_data['members']['logins']:
            print()
            print(f'Login: {user}')
            for key, value in self.gym_data['members']['logins'][user].items():
                print(f'{key}: {value}')
            yield (user, self.gym_data['members']['logins'][user])
        return "User\'s list ended"


    def delegator(self, generator: Generator[tuple[str, dict], None, str]) -> Generator[tuple[str, dict], None, None]:
        try:
            output = yield from generator
            print()
            print(f'{output}')
        except Exception as e:
            print(f"Error: {e}")


    def user_management(self, user_login: str, user_data: dict):
        clear_console()
        print(f"Login: {user_login}")
        for key, value in user_data.items():
            if key != "password":
                print(f"{key}: {value}")
        choice = int(input("1 - Add workouts\n"
                    "2 - Mark workout\n"
                    "3 - Ping user"))
        match choice:
            case 1:
                while True:
                    try:

                        count = int(input("Enter the number of workouts: "))
                        self.gym_data['members']['logins'][user_login]['workouts'] += count
                        logging.info(f'{user_login} gained {count} workouts')

                        break
                    except ValueError:
                        print("Enter a number")
            case 2:
                while True:
                    try:
                        
                        count = int(input("Enter the number of workouts: "))
                        self.gym_data['members']['logins'][user_login]['workouts'] -= count
                        logging.info(f'{user_login} lost {count} workouts')

                        break
                    except ValueError:
                        print("Enter a number")
            case 3:
                print("User pinged")
            case _:
                print('Unknown command')
        
        self.save_to_json(self.gym_data)


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