from classes.gymsystem import System
from utils import clear_console, DATA_PATH


system = System(DATA_PATH)


def main() -> None:
    clear_console()
    system.entrance()


if __name__ == "__main__":
    main()
