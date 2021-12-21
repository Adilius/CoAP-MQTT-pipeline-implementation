import sys

def handle(client_ID: str):
    print(f'\u001b[31m' +f'MQTT Broker| Client ID ({client_ID}) disconnected.' + '\033[0m')
    sys.exit()