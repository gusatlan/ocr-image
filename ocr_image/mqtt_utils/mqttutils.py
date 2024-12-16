import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
from utils.utils import get_logger
from os_utils.osutils import get_parameter


MQTT_HOST_ENV='mqtt_host'
MQTT_PORT_ENV='mqtt_port'
MQTT_USER_ENV='mqtt_user'
MQTT_PASSWORD_ENV='mqtt_password'
MQTT_TOPIC_COMMAND_ENV='mqtt_topic_command'
MQTT_TOPIC_WATER_ENV='mqtt_topic_water'


def get_mqtt_host() -> str:
    return get_parameter(env_variable=MQTT_HOST_ENV)


def get_mqtt_port() -> int:
    return int(get_parameter(env_variable=MQTT_PORT_ENV))


def get_mqtt_username() -> str:
    return get_parameter(env_variable=MQTT_USER_ENV)


def get_mqtt_password() -> str:
    return get_parameter(env_variable=MQTT_PASSWORD_ENV)


def get_mqtt_topic_command() -> str:
    return get_parameter(env_variable=MQTT_TOPIC_COMMAND_ENV)


def get_mqtt_topic_consumption() -> str:
    return get_parameter(env_variable=MQTT_TOPIC_WATER_ENV)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        get_logger().info('Successfuly connected!')
    else:
        get_logger().error('Error on connect: ', rc)


def create_client(
        host:str=get_mqtt_host(),
        port:int=get_mqtt_port(),
        username:str=get_mqtt_username(),
        password:str=get_mqtt_password()
    ) -> mqtt.Client:

    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(host, port)

    return client


def disconnect(client:mqtt.Client) -> None:
    get_logger().info('Disconnecting...')
    
    client.loop_stop()
    client.disconnect()
    
    get_logger().info('Disconnected')


def start(client:mqtt.Client) -> None:
    client.loop_start()


def send_message(client:mqtt.Client, topic:str=get_mqtt_topic_command(), message:str='ON'):
    result = client.publish(topic, message)

    status = result[0]
    if status == 0:
        get_logger().info(f'Published [{topic}][{message}]')
    else:
        get_logger().error('Error on publish message {topic}')
    
    return status
