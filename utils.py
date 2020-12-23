import os

from linebot import LineBotApi, WebhookParser
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
    ImageMessage, TemplateSendMessage, MessageAction,
    ImageCarouselTemplate, ImageCarouselColumn, ButtonsTemplate
)

from sql import Database

channel_access_token = os.getenv("LINE_CHANNEL_TOKEN", None)
line_bot_api = LineBotApi(channel_access_token)

def send_text_message(reply_token, text):
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"

def send_img_message(reply_token, img_url):
    msg = ImageSendMessage(
        original_content_url=img_url,
        preview_image_url=img_url
    )
    line_bot_api.reply_message(reply_token, msg)

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

def send_usage(reply_token):
    msg = TemplateSendMessage(
        alt_text='Linebot Usage',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/iaDRkA7.png',
            title='Memecraft', text='Creating memes from messages',
            actions=[
                MessageAction(
                    label='Browse templates', text='templates'
                ),
                MessageAction(
                    label='Upload memes', text='upload'
                ), 
                MessageAction(
                    label='View Gallery', text='gallery'
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, msg)

def send_gallery(reply_token, memes):
    # preprocess the info data
    columns = []
    for (idx, name, url) in memes:
        columns.append(
            ImageCarouselColumn(
                image_url=url,
                action=MessageAction(
                    label='Share now',
                    text='share'
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