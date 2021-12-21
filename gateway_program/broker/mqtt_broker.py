import socket, sys, time
from threading import Thread
from .mqtt import MQTT_decoder
from .mqtt import MQTT_database
from .mqtt.MQTT_packet_handler import packet_router
from .mqtt.MQTT_control_packets import PUBLISH

HOST = "127.0.0.1"
PORT = 1883

connected_clients = []


def run_server():
    print('\u001b[31m' +f'MQTT Broker| Starting on port {PORT}' + '\033[0m')
    main()


def main():
    # Initialize database
    MQTT_database.initialize_database()

    # Create dummy session and topic
    MQTT_database.topic_create('temperature')
    MQTT_database.topic_create('humidity')

    # Start broker server
    start_broker()


def start_broker():

    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind socket to port
    try:
        server_socket.bind((HOST, PORT))
        #print(f"Binding server socket to host: {HOST} and port: {PORT}")
    except:
        print(f'\u001b[31m' +f"MQTT Broker| Bind failed. \nError: {str(sys.exc_info())}" + '\033[0m')
        sys.exit()

    # Enable passive listening sockets
    server_socket.listen(5)

    # Periodically jump out of accept waiting process to receive keyboard interrupt commnad
    server_socket.settimeout(0.5)


    while True:

        client_socket = None

        try:
            # Wait and accept incoming connection
            (client_socket, address) = server_socket.accept()
            ip, port = str(address[0]), str(address[1])
            #print(f'\u001b[31m' +f"MQTT Broker| Connection from {ip}:{port} has been established." + '\033[0m')

            try:
                Thread(target=client_thread, args=(client_socket, ip, port)).start()
                #print(f'\u001b[31m' +f"MQTT Broker| Client thread for {ip}:{port} has been created." + '\033[0m')
            except:
                print(f'\u001b[31m' +f"MQTT Broker| Client thread for {ip}:{port} did not create" + '\033[0m')
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            sys.exit()


def client_thread(client_socket, ip, port):

    global connected_clients

    client_ID = ""

    while True:

        try:
            # Listen to incoming data
            try:
                data = client_socket.recv(1024)
            except:
                print(f'\u001b[31m' +f'MQTT Broker| Client ({client_ID}) unexpected disconnect.' + '\033[0m')
                connected_clients = [client for client in connected_clients if client_ID not in client]
                sys.exit()
            if not data:
                time.sleep(0.5)
                print(f'\u001b[31m' +f"MQTT Broker| Client ({client_ID}) went to sleep" + '\033[0m')
                break

            #print(f"Incomming packet: {data}")

            # Decode incoming packet
            incoming_packet = MQTT_decoder.decode(data)

            if incoming_packet.get("Packet type") == "CONNECT":
                client_ID = incoming_packet.get("Payload")
                connected_clients.append((client_ID, client_socket))

            if incoming_packet.get("Packet type") == "DISCONNECT":
                connected_clients = [client for client in connected_clients if client_ID not in client]

            # Do events & encode outgoing packet
            outgoing_packet = packet_router.route_packet(incoming_packet, client_ID)
            #print(f'Outgoing packet: {outgoing_packet}')


            # Send outgoing packet
            if incoming_packet.get("Packet type") == "PUBLISH":
                send_to_all_connected(outgoing_packet)
            else:
                client_socket.send(outgoing_packet)

            # Send publish packet that has been retained to new subscribers
            if incoming_packet.get("Packet type") == "SUBSCRIBE":
                topic = incoming_packet.get('Topics')[0]
                topic = next(iter(topic))
                if topic in MQTT_database.session_get_topic(client_ID):
                    if MQTT_database.topic_exists(topic):
                        value = MQTT_database.topic_get_value(topic)
                        outgoing_packet = PUBLISH.encode(topic, value)
                        client_socket.send(outgoing_packet)

        except KeyboardInterrupt:
            client_socket.close()
            sys.exit()


def send_to_all_connected(packet: bytes):
    global connected_clients

    for client in connected_clients:
        client_ID, client_socket = client
        client_socket.send(packet)
if __name__ == "__main__":
    main()
