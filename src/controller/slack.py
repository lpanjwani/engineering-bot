from src.agents.rag import RAGAgent
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
import logging
import os
from dotenv import load_dotenv

load_dotenv()

app_token = os.environ.get("SLACK_APP_TOKEN")
bot_token = os.environ.get("SLACK_BOT_TOKEN")


logger = logging.getLogger(__name__)


def SlackEventProcessor():
    rag_agent = RAGAgent()

    client = SocketModeClient(
        app_token=app_token,
        web_client=WebClient(token=bot_token),
        logger=logger,
        trace_enabled=True,
    )

    def ack(req: SocketModeRequest):
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

    def check_for_bot_or_throw(req: SocketModeRequest):
        if req.payload["event"].get("bot_id") is not None:
            raise Exception("Bot Event Loop Detected")

    def react_to_message(emoji: str, req: SocketModeRequest):
        client.web_client.reactions_add(
            name=emoji,
            channel=req.payload["event"]["channel"],
            timestamp=req.payload["event"]["ts"],
        )

    def post_message(text: str, client: SocketModeClient, req: SocketModeRequest):
        client.web_client.chat_postMessage(
            channel=req.payload["event"]["channel"],
            thread_ts=req.payload["event"]["ts"],
            text=text,
        )

    def process(client: SocketModeClient, req: SocketModeRequest):
        if req.type == "events_api":
            ack(req)
            check_for_bot_or_throw(req)

            if req.payload["event"]["type"] == "message":
                react_to_message("eyes", req)
                user_question = req.payload["event"]["text"]
                logging.info(f"Question: {user_question}")
                rag_response = rag_agent.ask(user_question)
                logging.info(f"Answer: {rag_response}")
                post_message(rag_response, client, req)

    client.socket_mode_request_listeners.append(process)

    client.connect()
