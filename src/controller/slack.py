import asyncio
import os
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from src.agents.rag import RAGAgent

app_token = os.environ.get("SLACK_APP_TOKEN")
bot_token = os.environ.get("SLACK_BOT_TOKEN")


async def SlackEventProcessor():
    from slack_sdk.socket_mode.response import SocketModeResponse
    from slack_sdk.socket_mode.request import SocketModeRequest

    rag_agent = RAGAgent()

    client = SocketModeClient(
        app_token=app_token, web_client=AsyncWebClient(token=bot_token)
    )

    async def ack(req: SocketModeRequest):
        response = SocketModeResponse(envelope_id=req.envelope_id)
        await client.send_socket_mode_response(response)

    async def check_for_bot_or_throw(req: SocketModeRequest):
        if req.payload["event"].get("bot_id") is not None:
            raise Exception("Bot Event Loop Detected")

    async def react_to_message(emoji, req: SocketModeRequest):
        await client.web_client.reactions_add(
            name=emoji,
            channel=req.payload["event"]["channel"],
            timestamp=req.payload["event"]["ts"],
        )

    async def post_message(text, client: SocketModeClient, req: SocketModeRequest):
        await client.web_client.chat_postMessage(
            channel=req.payload["event"]["channel"], text=text
        )

    async def process(client: SocketModeClient, req: SocketModeRequest):
        if req.type == "events_api":
            await ack(req)
            await check_for_bot_or_throw(req)

            if req.payload["event"]["type"] == "message":
                await react_to_message("eyes", req)
                user_question = req.payload["event"]["text"]
                rag_response = await rag_agent.ask(user_question)
                await post_message(rag_response, client, req)

    client.socket_mode_request_listeners.append(process)

    await client.connect()

    await asyncio.sleep(float("inf"))
