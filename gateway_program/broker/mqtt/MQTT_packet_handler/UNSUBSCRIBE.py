from ..MQTT_control_packets import UNSUBACK
from .. import MQTT_database
import sys

def handle(incoming_packet: dict, client_ID):

    # Get packet identifier
    packet_identifier = incoming_packet.get('Packet identifier')

    # Get topics
    topics = incoming_packet.get('Topics')

    # Get flags
    flags = incoming_packet.get('Flags')
    if flags != "0010": # Malformed packet
        sys.exit()

    # remove topics from client
    for topic in topics:
        MQTT_database.session_remove_topic(client_ID, topic)
        print(f'\u001b[31m' +f'MQTT Broker| Client ID ({client_ID}) unsubscribed to ({topic})' + '\033[0m')

    # create packet
    outgoing_packet = UNSUBACK.encode(packet_identifier)
    return outgoing_packet
