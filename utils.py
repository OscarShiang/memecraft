import os

from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    TemplateSendMessage, MessageAction,
    ImageCarouselTemplate, ImageCarouselColumn
)

from sql import Database

channel_access_token = os.getenv("LINE_CHANNEL_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_templates(reply_token, alt_text, info):
    # preprocess the info data
    columns = []
    for (idx, name, url) in info:
        columns.append(
            ImageCarouselColumn(
                image_url=url,
                action=MessageAction(
                    label='Use this',
                    text=name
                )
            )
        )

    # compile the message
    msg = TemplateSendMessage(
        alt_text='Image template test',
        template=ImageCarouselTemplate(
            columns=columns
        )
    )
    line_bot_api.reply_message(reply_token, msg)

    return 'OK'