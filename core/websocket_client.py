import asyncio
import websockets
import json
import logging

class WebSocketClient:
    def __init__(self, url, on_message):
        self.url = url
        self.on_message = on_message
        self.should_run = True

    async def run(self):
        while self.should_run:
            try:
                logging.info(f"Connecting to WebSocket: {self.url}")
                async with websockets.connect(
                    self.url,
                    ping_interval=20,
                    ping_timeout=30,
                    close_timeout=6,
                ) as ws:
                    logging.info("WebSocket connected.")
                    # Send connection status update
                    await self.on_message({"connection_status": "connected"})
                    async for msg in ws:
                        try:
                            # Log message size for debugging performance
                            msg_size = len(msg)
                            logging.debug(f"Received WebSocket message of size {msg_size} bytes")
                            
                            # Parse and process the message
                            data = json.loads(msg)
                            await self.on_message(data)
                        except json.JSONDecodeError:
                            logging.error(f"Invalid JSON received: {msg[:100]}...")
            except Exception as e:
                logging.error(f"WebSocket error: {e}")
                # Send disconnection status update
                await self.on_message({"connection_status": "disconnected"})
                await asyncio.sleep(5)

    def stop(self):
        self.should_run = False
