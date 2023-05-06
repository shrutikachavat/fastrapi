from django.core.management.base import BaseCommand
from fastrapibase.arduino_script import scan_rfid
import requests


class Command(BaseCommand):
    help = 'Scans RFID card data from the Arduino'

    def handle(self, *args, **options):

        KART_TOKEN_URL = "http://localhost:8000/token/create/"
        data = {'email': 'user@fastr.com', 
                'password': 'Test@123'}

        response = requests.post(url=KART_TOKEN_URL, 
                                 data=data)
        try:
            auth_token = response.request.headers.get('Cookie').split('"')[1]
        except Exception:
            auth_token = None
        print(auth_token)

        while True:
            scan_rfid(auth_token)