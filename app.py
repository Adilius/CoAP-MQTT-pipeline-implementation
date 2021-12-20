import asyncio
from threading import Thread
import sys, os, time

from sensor_program import coap_server
from gateway_program.client import gateway_client
from gateway_program.broker import mqtt_broker
from user_interface_program.client import mqtt_client
from user_interface_program.front_end import flask_server

def main():

    # Servers
    Thread(target=coap_server.run_server).start()
    Thread(target=mqtt_broker.run_server).start()
    Thread(target=flask_server.run_server).start()

    # Start clients
    Thread(target=gateway_client.run_client).start()
    Thread(target=mqtt_client.run_client).start()

    # Wait for keyboard interrupt to kill all threads
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            os._exit(0)

if __name__ == "__main__":
    main()
