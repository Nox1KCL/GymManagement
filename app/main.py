from classes.admin import Admin
from classes.gymsystem import System
from utils import clear_console, DATA_PATH, hash_password


system = System(DATA_PATH)


def main():
    clear_console()
    system.entrance()

if __name__ == "__main__":
    main()
