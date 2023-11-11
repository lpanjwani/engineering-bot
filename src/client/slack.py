from ast import Not
import asyncio
import os
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient

app_token = os.environ.get("SLACK_APP_TOKEN")
bot_token = os.environ.get("SLACK_BOT_TOKEN")

async def SlackEventProcessor():
    from slack_sdk.socket_mode.response import SocketModeResponse
    from slack_sdk.socket_mode.request import SocketModeRequest

    client = SocketModeClient(
        app_token=app_token,
        web_client=AsyncWebClient(token=bot_token) 
    )

    async def ack(req: SocketModeRequest):
        response = SocketModeResponse(envelope_id=req.envelope_id)
        await client.send_socket_mode_response(response)

    async def check_for_bot_or_throw(req: SocketModeRequest):
        if req.payload["event"].get("bot_id") is not None:
            raise Exception("Bot Event Loop Detected")

    async def process(client: SocketModeClient, req: SocketModeRequest):
        if req.type == "events_api":
            await ack(req)
            
            await check_for_bot_or_throw(req)

            if req.payload["event"]["type"] == "message" \
                and req.payload["event"].get("subtype") is None:
                await client.web_client.reactions_add(
                    name="eyes",
                    channel=req.payload["event"]["channel"],
                    timestamp=req.payload["event"]["ts"],
                )

                await client.web_client.chat_postMessage(
                    channel=req.payload["event"]["channel"],
                    text=":wave: Hi there!"
                )


    client.socket_mode_request_listeners.append(process)

    await client.connect()

    await asyncio.sleep(float("inf"))

asyncio.run(SlackEventProcessor())