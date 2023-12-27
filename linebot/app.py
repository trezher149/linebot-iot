from fastapi import FastAPI, Request, HTTPException
from pyngrok import ngrok
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.messaging.models.set_webhook_endpoint_request import SetWebhookEndpointRequest
from linebot.v3.messaging.models.test_webhook_endpoint_request import TestWebhookEndpointRequest
from linebot.v3.messaging.models.test_webhook_endpoint_response import TestWebhookEndpointResponse
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.v3 import (
    WebhookHandler
)

from dotenv import load_dotenv
import asyncio
import os
from pymongo import MongoClient
import pymongo
import json

load_dotenv()

app = FastAPI()
ngrok.set_auth_token(os.environ.get("NGROK_TOKEN"))
public_url = ngrok.connect(os.environ["WEBHOOK_PORT"]).public_url
print(public_url)

configuration = Configuration(
    access_token=os.environ.get("LINE_ACCESS_TOKEN"),
)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(os.environ.get("LINE_CHANNEL_SECRET"))
handler = WebhookHandler('NGROK_TOKEN')

usrname = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
passwd = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
mongo_client = MongoClient(f"mongodb://{usrname}:{passwd}@linebot-iot-mongodb-1:27017/")
db = mongo_client.test_database
collection = db.test_collection

@app.get("/")
async def init_bot():
    set_webhook_endpoint_request = SetWebhookEndpointRequest(endpoint=public_url + "/callback")
    await line_bot_api.set_webhook_endpoint(set_webhook_endpoint_request)
    post = collection.find_one(sort= [( '_id', pymongo.DESCENDING)])
    post.pop("_id")
    return post

@app.post("/callback")
async def handle_callback(request: Request):
    lineText = ""
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = await request.body()
    body = body.decode()
    print(body)
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue
        if 'temperature' in event.message.text:
            post = collection.find_one(sort= [( '_id', pymongo.DESCENDING)])
            tem_only = post["temperature"]
            lineText += " temperature " + json.dumps(tem_only) + " °C "
        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=lineText)]
            )
        )
    return 'OK'