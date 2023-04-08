# ##########################CODE###################################################
# # import requests
# # import serial
# # from django.core.management.base import BaseCommand

# # ARDUINO_PORT = '/dev/tty.usbmodem14101'
# # ARDUINO_BAUDRATE = 9600

# # FASTRKART_PRODUCT_ADD_URL = 'http://localhost:8000/fastrkart/product/add/'

# # class Command(BaseCommand):
# #     help = 'Read RFID tag and make API call'

# #     def handle(self, *args, **options):
# #         # Open the serial connection to the Arduino
# #         ser = serial.Serial(port=ARDUINO_PORT, 
# #                             baudrate=ARDUINO_BAUDRATE)

# #         while True:
# #             try:
# #                 # Wait for an RFID tag to be scanned
# #                 tag_id = ser.readline().strip().decode()

# #                 # Make an API call to your Django app with the tag ID
# #                 url = FASTRKART_PRODUCT_ADD_URL
# #                 product_data = {'tag_id': tag_id}
# #                 response = requests.post(url,
# #                                         params=product_data)

# #                 # Print the API response
# #             except Exception as e:
# #                 print(e)
# #             else:
# #                 print(response.text)

# #         # Close the serial connection
# #         ser.close()
# ##################################################################################

# import requests
# import serial

# ARDUINO_PORT = '/dev/tty.usbmodem14101'
# ARDUINO_BAUDRATE = 9600

# PRODUCT_DETAILS_URL = "http://localhost:8000/product/products/"

# def rfid_card_present():
#     ser = serial.Serial()
#     ser.baudrate = ARDUINO_BAUDRATE
#     ser.port = ARDUINO_PORT
#     ser.open()
#     raw_data = ser.readline()
#     if raw_data:
#         raw_data = raw_data.decode()
#         raw_data = raw_data.strip()
#         return raw_data

# def tag_id_provider(tag_id):
#     return tag_id

# while True:
#     RFID_DATA = rfid_card_present()
#     if RFID_DATA:
#         print(tag_id_provider(RFID_DATA))

# ###########################################################################
# # # import requests

# # # def auth_token_generator(email, password):
# # #     data = {"email":email,
# # #             "password":password}
# # #     res = requests.post(url=USER_TOKEN_URL,
# # #                         data=data)
# # #     token = eval(res.text).get("token", None)
# # #     return token

# # # def fastrkart_product_add(token, product_tag_id):
# # #     product_data = {"quantity": 1}
# # #     product_data["tag_id"] = product_tag_id
# # #     header = {"Authorization": f"Token {token}"}
# # #     res = requests.post(url=PRODUCT_ADD_URL,
# # #                         headers=header,
# # #                         params=product_data)
# # #     print(res.text)

# # # PRODUCT_ADD_URL = "http://localhost:8000/fastrkart/product/add/"
# # # USER_TOKEN_URL = "http://localhost:8000/token/create/"
# # # USER_DETAILS_URL = "http://localhost:8000/user/user/"


# # def user_details(token):
# #     header = {"Authorization": f"Token {token}"}
# #     res = requests.get(url=USER_DETAILS_URL,
# #                        headers=header)
# #     print(res.text)