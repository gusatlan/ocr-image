from PIL import Image
import pytesseract
from utils.utils import get_logger
import base64
import os
import subprocess
from datetime import datetime
import pytz
from os_utils.osutils import get_parameter
import cv2

RTSP_PATH_ENV='rtsp_path'


def get_rtsp_path():
    return get_parameter(env_variable=RTSP_PATH_ENV)


def read_image(path:str):
    try:
        image = Image.open(path) 
        get_logger().info(f'Image [{path}]')
        return image
    except Exception as e:
        get_logger().error(f'Error on acquire image [{path}]', e)


def extract_text(image) -> str:
    try:
        metric = pytesseract.image_to_string(image=image, timeout=5)
        get_logger().info(f'Metric [{metric}]')
        return metric
    except RuntimeError as timeout_error:
        get_logger().error('Error on extract values from image', timeout_error)


def convert_image_base64_dict(image_base64, mime_type:str='image/jpeg'):
    content = {
          'mime_type': mime_type,
          'data': image_base64
        }
    return content


def now():
    timezone = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(timezone)
    return current_time
    

def save_image(url:str, target_dir:str):
    target = os.path.join(target_dir, f'{now()}.jpeg')
    command = ['ffmpeg', '-i', url, '-vframes', '1', '-q:v', '2', target]

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    try:
        subprocess.run(command, check=True)
        get_logger().info('Image captured', target)
    except subprocess.CalledProcessError as e:
        get_logger().error('Error on capture image', e)


def crop_image(file:str, x1:int, y1:int, x2:int, y2:int):
    image = cv2.imread(file)
    crop = image[y1:y2, x1:x2]
    cv2.imwrite(file, crop)