import requests
import paho.mqtt.client as mqtt
import time
import asyncio

# Адрес сервера
SERVER_URL = "http://192.168.31.145:8005"

# MQTT брокер
MQTT_BROKER = "broker.emqx.io"
MQTT_TOPIC_PREFIX = "led/"

# Функция для получения данных о комбинации цветов для устройства
async def get_combination_data():
    response = requests.get(f"{SERVER_URL}/admin")
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch combination data")
        return None

# Функция для отправки комбинации цветов по MQTT
def send_color_to_device(device_name, color_hex_code):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_BROKER)

    topic = f"{MQTT_TOPIC_PREFIX}{device_name}"

    client.publish(topic, color_hex_code)
    print(f"Color {color_hex_code} sent to device {device_name}")

async def pub():
    while True:
        combination_data = await get_combination_data()
        if combination_data:
            for device_data in combination_data:
                device_name = device_data["device_name"]
                color_hex_code = device_data["color_hex_code"]
                send_color_to_device(device_name, color_hex_code)

        await asyncio.sleep(5)
loop = asyncio.get_event_loop()
loop.run_until_complete(pub())

