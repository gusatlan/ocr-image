import os
import base64
from datetime import datetime
from utils.utils import get_logger

SOURCE_DIR_ENV='source_dir'
TARGET_DIR_ENV='target_dir'
FILE_SOURCE_EXTENSIONS_ENV='file_source_extensions'
SCHEDULE_ENV='schedule_minutes'
TIMEOUT_CAMERA_ONLINE_ENV='timeout_camera_online'


def get_parameter(env_variable:str) -> str:
    env_variable_formatted = env_variable.upper().strip()
    value = os.environ[env_variable_formatted]
    
    get_logger().info(f'[{env_variable_formatted}]=[{value}]')

    return value
    

def get_source_dir() -> str:
    return get_parameter(env_variable=SOURCE_DIR_ENV)


def get_target_dir() -> str:
    return get_parameter(env_variable=TARGET_DIR_ENV)


def get_source_file_extensions() -> list:
    value = get_parameter(env_variable=FILE_SOURCE_EXTENSIONS_ENV).split(',')
    value = list([x.strip().lower() for x in value])
    return value


def get_schedule_minutes() -> int:
    return int(get_parameter(env_variable=SCHEDULE_ENV))


def get_timeout_camera_online() -> int:
    return int(get_parameter(env_variable=TIMEOUT_CAMERA_ONLINE_ENV))



def read_source(path:str, extensions:list) -> list:
    files = []

    get_logger().info(f'Scanning source directory {path}')

    if not os.path.exists(path):
        get_logger().warning(f'Directory does not exist, creating {path}')
        os.makedirs(path)

    for file in os.listdir(path):
        full_path = os.path.join(path, file)

        get_logger().info(f'Verifying {file}')

        if os.path.isdir(full_path):
            [files.append(f) for f in read_source(path=full_path, extensions=extensions)]
        elif file.lower().endswith(tuple(extensions)):
            files.append(os.path.join(path, file))
            get_logger().info(f'Matched {file}')
    
    return files


def build_current_target_dir(target_dir:str) -> str:
    date = datetime.now()
    current_target_dir = os.path.join(target_dir, str(date.year), str(date.month), str(date.day))

    return current_target_dir


def read_file_base64(path:str) -> str:
    encoded = None

    with open(path, 'rb') as file:
        image_data = file.read()
        encoded = base64.b64encode(image_data).decode('utf-8')
    
    return encoded


def remove_file(dir:str,file:str) -> None:
    fullpath = os.path.join(dir, file)

    if os.path.exists(fullpath):
        os.remove(fullpath)
        get_logger().info(f'File removed {fullpath}')
    else:
        get_logger().error(f'File not exists {fullpath}')
