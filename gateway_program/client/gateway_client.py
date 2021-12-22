from .coap import coap_client
from .mqtt import mqtt_client
import time

def run_client():

    
    time.sleep(1)

    # Create CoAP client
    c_ip, c_port = '127.0.0.1', 5683
    c_client = coap_client.client(c_ip, c_port)
    print(f'\u001b[33m' + f'CoAP client| Connected to {c_ip}:{c_port}' + '\033[0m')

    # Create MQTT client
    m_ip, m_port = '127.0.0.1', 1883
    m_client = mqtt_client.client(m_ip, m_port)
    print(f'\u001b[36m' +f'MQTT client| Connected to {m_ip}:{m_port}' + '\033[0m')
    time.sleep(1)

    while True:

        topic = 'temperature'
        try:
            # Get value from CoAP server
            value = c_client.request_value(topic)

            # Decode from bytes to string
            decoded_value = value[0].decode()
        except:
            print(f'\u001b[33m' + f'CoAP client| Error getting sensor data')


        try:
            # Send value to MQTT Broker
            m_client.send_value(topic, decoded_value)
        except:
            print(f'\u001b[36m' +f'MQTT client| Error sending sensor data' + '\033[0m')


        time.sleep(5)  # Get and push new values to broker at this interval

        topic = 'humidity'
        try:
            # Get value from CoAP server
            value = c_client.request_value(topic)

            # Decode from bytes to string
            decoded_value = value[0].decode()
        except:
            print(f'\u001b[33m' + f'CoAP client| Error getting sensor data')


        try:
            # Send value to MQTT Broker
            m_client.send_value(topic, decoded_value)
        except:
            print(f'\u001b[36m' +f'MQTT client| Error sending sensor data' + '\033[0m')

        time.sleep(5)  # Get and push new values to broker at this interval
