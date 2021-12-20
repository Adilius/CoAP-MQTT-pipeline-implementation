import paho.mqtt.client as mqtt
import time

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f'\u001b[35m' +f'MQTT Front | New publish in {msg.topic}: {(msg.payload).decode()}' + '\033[0m')

class client():
    def __init__(self, ip_address, PORT, topic):
        self.mqtt_c = mqtt.Client(client_id="Frontend", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.mqtt_c.on_message = on_message
        time.sleep(2)
        self.connect(ip_address, PORT)
        time.sleep(1)
        self.subscribe(topic)
        time.sleep(1)
        self.mqtt_c.loop_forever()

    def connect(self, ip_address, PORT):
        self.mqtt_c.connect(ip_address, PORT, 60)
        print(f'\u001b[35m' +f'MQTT Front | Connected to {ip_address}:{PORT}' + '\033[0m')

    def subscribe(self, topic):
        self.mqtt_c.subscribe((topic, 0))
        print(f'\u001b[35m' +f'MQTT Front | Subscribed to {topic}' + '\033[0m')

def run_client():
    m_client = client('127.0.0.1', 1883, "temperature")
    pass
