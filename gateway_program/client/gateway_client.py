from .coap import coap_client
from .mqtt import mqtt_client
import time

def run_client():

    topic = 'temperature'

    print('Gateway clients starting...')
    time.sleep(3.14)

    # Create CoAP client
    c_client = coap_client.client('127.0.0.1', 5683)

    # Create MQTT client
    m_client = mqtt_client.client('127.0.0.1', 1883)

    while True:
        try:
            # Get value from CoAP server
            print()
            value = c_client.request_value(topic)

            # Decode from bytes to string
            decoded_value = value[0].decode()

            # Send value to MQTT Broker
            m_client.send_value(topic, decoded_value)
        except:
            print('Error getting sensor data')
        finally:
            time.sleep(60)
