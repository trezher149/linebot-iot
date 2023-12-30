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
from linebot.models import FollowEvent, UnfollowEvent

mongo_host = os.environ["MONGO_HOST"]
usrname = os.environ["MONGO_INITDB_ROOT_USERNAME"]
passwd = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
mongo_client = MongoClient(f"mongodb://{usrname}:{passwd}@{mongo_host}")

load_dotenv()

app = FastAPI()
ngrok.set_auth_token(os.environ.get("NGROK_TOKEN"))
public_url = ngrok.connect(os.environ["WEBHOOK_PORT"]).public_url
print(public_url)

configuration = Configuration(
    access_token=os.environ["LINE_ACCESS_TOKEN"],
)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(os.environ["LINE_CHANNEL_SECRET"])
handler = WebhookHandler('NGROK_TOKEN')

@app.get("/")
async def init_bot():
    set_webhook_endpoint_request = SetWebhookEndpointRequest(endpoint=public_url + "/callback")
    await line_bot_api.set_webhook_endpoint(set_webhook_endpoint_request)
    return 'Hello, World!'


@app.post("/callback")
async def handle_callback(request: Request):
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
        if event.message.text.lower() == 'report':
            # Get the latest data from your MongoDB
            iot_data = get_iot_data()
            if iot_data:
                message = f"Timestamp: {iot_data['timestamp']}\n"
                message += f"Temperature HTS: {iot_data['temperature hts']}°C\n"
                message += f"Humidity HTS: {iot_data['humidity hts']}%\n"
                message += f"Temperature BMP: {iot_data['temperature bmp']}°C\n"
                message += f"Pressure BMP: {iot_data['pressure bmp']} hPa"
                await line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text=message)]
                    )
                )
        else:
            await line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="Please type 'Report'")]
                )
            )
    return 'OK'

def get_iot_data():
    db = mongo_client.test_database
    collection = db.test_collection
    # ค้นหาข้อมูลล่าสุดโดยเรียงตาม _id แบบลดลง
    latest_data = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
    if latest_data:
        return {
            "timestamp": latest_data["timestamp"],
            "temperature hts": latest_data["temperature hts"],
            "humidity hts": latest_data["humidity hts"],
            "temperature bmp": latest_data["temperature bmp"],
            "pressure bmp": latest_data["pressure bmp"]
        }
    else:
        return None
