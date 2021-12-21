import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

from .sensor_data import sensor

HOST = '127.0.0.1'
PORT = 5683

class temperature_resource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.sensor = sensor()

    async def render_get(self, request):
        payload = self.sensor.get_sensor_data()
        print(f'\u001b[32m' +f'CoAP client| GET /temperature with payload: {payload.decode()}' + '\033[0m')
        return aiocoap.Message(payload=payload)

async def main():

    # Resource tree creation
    root = resource.Site()
    root.add_resource(['temperature'], temperature_resource())

    # Binds context to all adresses on CoAP port
    await aiocoap.Context.create_server_context(bind=(HOST,PORT),site=root)

    # Server loop
    await asyncio.get_running_loop().create_future()


def run_server():
    print('\u001b[32m' +f"CoAP server| Starting on port {PORT}" + '\033[0m')

    # logging setup
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("coap-server").setLevel(logging.INFO)

    asyncio.run(main())

if __name__ == "__main__":
    run_server()
