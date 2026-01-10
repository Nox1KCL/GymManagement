import logging
import os
from pathlib import Path
import uuid
import hashlib


LOG_DIR = Path(__file__).parent
LOG_PATH = LOG_DIR / 'logging' / 'app.log'

DATA_DIR = Path(__file__).parent
DATA_PATH = DATA_DIR / 'userdata' / 'data.json'


logging.basicConfig (
    filename=LOG_PATH,    
    level=logging.INFO,        
    encoding='utf-8',          
    format='%(asctime)s - %(levelname)s - %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_mac_address(self) -> str:
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')