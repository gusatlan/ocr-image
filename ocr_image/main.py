from os_utils.osutils import get_source_dir, get_source_file_extensions, read_source, read_file_base64, remove_file, get_schedule_minutes, get_timeout_camera_online, is_backup, get_backup_dir, backup_file
from image_utils.imageutils import read_image, extract_text, convert_image_base64_dict, save_image, get_rtsp_path, crop_image
from ai_utils.aiutils import chat_with_gemini, extract_value, get_ai_prompt
from mqtt_utils.mqttutils import create_client, start, disconnect, send_message, get_mqtt_topic_command, get_mqtt_topic_consumption
from datetime import datetime
from utils.utils import get_logger
import json
from dotenv import load_dotenv
import time
import schedule


def read_images() -> list[str]:
    return read_source(path=get_source_dir(), extensions=get_source_file_extensions())


def extract_values(files:list[str]) -> list[str]:
    metrics = []

    for file in files:
        image = read_image(path=file)
        metric = extract_text(image=image)
        metrics.append(metric)

    return metrics


def save_frame():
    save_image(url=get_rtsp_path(), target_dir=get_source_dir())


def read_job():
    load_dotenv()
    client_mqtt = create_client()
    start(client=client_mqtt)
    send_message(client=client_mqtt, message='ON')

    timeout_camera= get_timeout_camera_online()
    get_logger().info(f'Waiting {timeout_camera} seconds for camera online')
    time.sleep(timeout_camera)
    get_logger().info('Wait complete')

    save_frame()
    files = read_images()
    [crop_image(file=file, x1=4, y1=32, x2=632, y2=336) for file in files]

    images = [read_file_base64(file) for file in files]
    images_base64 = [convert_image_base64_dict(image_base64=image) for image in images]

    try:
        response = extract_value(text=chat_with_gemini(
            prompt=get_ai_prompt(),
            image=images_base64[0]
        ))

        response_json = json.dumps({'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'consumption': float(response), 'entity': 'house3_water'})

        get_logger().info(f'Result to send:{response_json}')
        send_message(client=client_mqtt, topic=get_mqtt_topic_consumption(), message=response_json)
        get_logger().info(f'Water consumption {response_json}')
    except Exception as err:
        get_logger().error('Error on extract value', err)
    finally:
        send_message(client=client_mqtt, topic=get_mqtt_topic_command(), message='OFF')
        disconnect(client=client_mqtt)

    if is_backup():
        [backup_file(src_dir=get_source_dir(), src_file=file, target_dir=get_backup_dir()) for file in files]
    
    [remove_file(dir=get_source_dir(), file=file) for file in files]
    


if __name__ == '__main__':

    get_logger().info('Job initialized')
    schedule.every(get_schedule_minutes()).minutes.do(read_job)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        schedule.clear()
    
    

    #for file in files:
    #    response = chat_with_gpt(
    #        prompt='Qual a leitura de água? Retorne apenas o valor numérico da leitura',
    #        image_type='image/jpg',
    #        image=read_file_base64(file),
    #        max_tokens=300,
    #        temperature=0.7
    #    )

    #response = chat_with_ollama(
    #    host=get_ai_host(),
    #    model=get_ai_model(),
    #    prompt=get_ai_prompt(),
    #    images=files
    #)

    #response = extract_value(text=chat_with_gemini(
    #    prompt=get_ai_prompt(),
    #    image=images_base64[0]
    #))
