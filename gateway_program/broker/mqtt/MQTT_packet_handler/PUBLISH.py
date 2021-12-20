from ..MQTT_control_packets import PUBLISH
from .. import MQTT_database

def handle(incoming_packet: dict, client_ID: str):

    topic = incoming_packet.get('Topic')
    payload = incoming_packet.get('Payload')

    # Update topic
    if MQTT_database.topic_update_value(topic, payload):
        print(f'\u001b[31m' +f'MQTT Broker| Client ID ({client_ID}) updated topic ({topic}) updated value to: {payload}' + '\033[0m')

    # Create publish packet
    outgoing_packet = PUBLISH.encode(topic, payload)
    return outgoing_packet