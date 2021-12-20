import paho.mqtt.client as mqtt

class client():
    def __init__(self, ip_address, PORT):
        self.mqtt_c = mqtt.Client(client_id="Gateway", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.mqtt_c.connect(ip_address, PORT, 60)

    def send_value(self, topic, payload):
        self.mqtt_c.publish(topic=topic, payload=payload)
        pass
