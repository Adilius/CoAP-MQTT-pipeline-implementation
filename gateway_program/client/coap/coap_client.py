import socket
from . import CoAP_encoder
from . import CoAP_decoder

class client():
    def __init__(self, ip_address, PORT):
        # Connection settings
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5)
        self.client_socket.connect((ip_address , PORT))

        # Query parameters
        self.method = 'GET'
        self.path = 'temperature'

    def request_value(self, path):
        # Build packet
        built_packet = CoAP_encoder.build_packet(
        method = self.method,
        option = 11,
        option_value = path)

        # Send packet
        self.client_socket.send(built_packet)

        # Recieve response
        try:
            recieved_data = self.client_socket.recv(1024)
        except TimeoutError:
            print('Recieving packet timed out...')
            return None
        else:
            # Decode & print packet
            decoded_packet = CoAP_decoder.decode_packet(recieved_data)
            return decoded_packet[-1:]
