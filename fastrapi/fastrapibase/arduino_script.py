from django.conf import settings
import serial
import requests

def rfid_card_present():
    ser = serial.Serial()
    ser.baudrate = settings.ARDUINO_BAUDRATE
    ser.port = settings.ARDUINO_PORT
    ser.open()
    raw_data = ser.readline()
    if raw_data:
        raw_data = raw_data.decode()
        raw_data = raw_data.strip()
        return raw_data

def tag_id_provider(tag_id):
    return tag_id

def scan_rfid(auth_token):
    RFID_DATA = rfid_card_present()
    if RFID_DATA:
        tag_id = tag_id_provider(RFID_DATA)

        PRODUCT_ADD_URL = "http://localhost:8000/fastrkart/product/add/"
        params = {'tag_id': f'{tag_id}'}
        headers = {'Authorization': f'{auth_token}'}

        response = requests.post(url=PRODUCT_ADD_URL,
                                 headers=headers,
                                 params=params)
        print(f"Checked {tag_id}, status_code {response.status_code}")
        return {"tag_id": f"{tag_id}",
                "status_code": response.status_code}
        