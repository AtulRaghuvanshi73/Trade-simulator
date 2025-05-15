import asyncio
import websockets
import json

class WebSocketClient:
    def __init__(self, url, on_message):
        self.url = url
        self.on_message = on_message
        self.should_run = True

    async def run(self):
        while self.should_run:
            try:
                async with websockets.connect(self.url) as ws:
                    async for msg in ws:
                        data = json.loads(msg)
                        await self.on_message(data)
            except Exception as e:
                print(f"WebSocket error: {e}")
                await asyncio.sleep(2)

    def stop(self):
        self.should_run = False
