import datetime
import logging
import asyncio
import aiocoap.resource as resource
import aiocoap

from .sensor_data import sensor


class temperature_resource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.sensor = sensor()

    async def render_get(self, request):
        payload = self.sensor.get_sensor_data()
        print(f'CoAP server respond to GET /temperature with payload: {payload.decode()}')
        return aiocoap.Message(payload=payload)

async def main():

    # Resource tree creation
    root = resource.Site()
    root.add_resource(['temperature'], temperature_resource())

    # Binds context to all adresses on CoAP port
    await aiocoap.Context.create_server_context(bind=('127.0.0.1',5683),site=root)

    # Server loop
    await asyncio.get_running_loop().create_future()


def run_server():
    print("CoAP server running...")

    # logging setup
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("coap-server").setLevel(logging.INFO)

    asyncio.run(main())

if __name__ == "__main__":
    run_server()
