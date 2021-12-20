import asyncio
from threading import Thread
import sys, os, time

from sensor_program import coap_server
from gateway_program.client import gateway_client


def main():

    # Start sensor program
    Thread(target=coap_server.run_server).start()
    Thread(target=gateway_client.run_client).start()


    # Wait for keyboard interrupt to kill all threads
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            os._exit(0)

if __name__ == "__main__":
    main()
