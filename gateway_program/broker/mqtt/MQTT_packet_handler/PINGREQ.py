from ..MQTT_control_packets import PINGRESP

def handle(client_ID: str):
    outgoing_packet = PINGRESP.encode(client_ID)
    return outgoing_packet