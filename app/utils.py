# region Imports

import logging
import os
from pathlib import Path
import uuid
import hashlib

# endregion

LOG_DIR = Path(__file__).parent
LOG_PATH = LOG_DIR / 'logging' / 'app.log'

DATA_DIR = Path(__file__).parent
DATA_PATH = DATA_DIR / 'userdata' / 'data.json'


NAME_MIN_LEN, NAME_MAX_LEN = 3, 10
PASSWORD_MIN__LEN, PASSWORD_MAX__LEN = 6, 24
WORKOUT_MIN_COUNT, WORKOUT_MAX_COUNT = 1, 10


logging.basicConfig (
    filename=LOG_PATH,    
    level=logging.INFO,        
    encoding='utf-8',          
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_mac_address() -> str:
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))


def clear_console() -> None:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def validate_username(name: str) -> bool:
    """Validates if the username length is between 3 and 10 characters."""
    return NAME_MIN_LEN <= len(name) <= NAME_MAX_LEN


def validate_password(password: str) -> bool:
    """Validates if the password length is between 6 and 24 characters."""
    return PASSWORD_MIN__LEN <= len(password) <= PASSWORD_MAX__LEN


def validate_workouts(workouts: int) -> bool:
    """Validates if the workout count is between 1 and 10."""
    return WORKOUT_MIN_COUNT <= workouts <= WORKOUT_MAX_COUNT