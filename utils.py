import os

import urllib3
from linebot import LineBotApi, WebhookParser
from linebot.models import (ButtonsTemplate, CarouselColumn, CarouselTemplate,
                            ImageCarouselColumn, ImageCarouselTemplate,
                            ImageMessage, ImageSendMessage, MessageAction,
                            MessageEvent, TemplateSendMessage, TextMessage,
                            TextSendMessage)

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

def send_templates_menu(reply_token):
    msg = TemplateSendMessage(
        alt_text='Select the kind of template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/TZUeq4A.png',
                    title='Memes',
                    text='Share your ideas with friends',
                    actions=[
                        MessageAction(
                            label='Choose it',
                            text='show_memes'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/14aCD1P.jpg',
                    title="Grandparents' blessings",
                    text='Give away warm greetings',
                    actions=[
                        MessageAction(
                            label='Choose it',
                            text='show_blesses'
                        )
                    ]
                )
            ]
        )
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

def send_menu(reply_token):
    msg = TemplateSendMessage(
        alt_text='Memecraft Menu',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/iaDRkA7.png',
            title='Memecraft', text='Creating memes from messages',
            actions=[
                MessageAction(
                    label='Browse templates', text='templates'
                ),
                MessageAction(
                    label='Upload memes', text='upload_image'
                ), 
                MessageAction(
                    label='View gallery', text='gallery'
                ),
                MessageAction(
                    label='Show usages', text='usage'
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, msg)

def send_usage(reply_token):
    msg = TemplateSendMessage(
        alt_text='Memecraft Usages',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/PZCJwp6.png',
                    title='Make memes',
                    text='Creating your own memes with templates',
                    actions=[
                        MessageAction(
                            label='Try it',
                            text='templates'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/m8xhUiD.png',
                    title="Upload works",
                    text='Share your creativity with others',
                    actions=[
                        MessageAction(
                            label='Try it',
                            text='upload_image'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/ncpaICm.png',
                    title="View gallery",
                    text='View great works in meme gallery',
                    actions=[
                        MessageAction(
                            label='Try it',
                            text='gallery'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(reply_token, msg)

def send_gallery(reply_token, memes):
    # preprocess the info data
    columns = []
    for i, (idx, name, url) in enumerate(memes):
        columns.append(
            ImageCarouselColumn(
                image_url=url,
                action=MessageAction(
                    label='Share now',
                    text=f'show_gallery_{i}'
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

def getImageFromLineAPI(msgId):
    http = urllib3.PoolManager()
    header = {
        'Authorization': f'Bearer {channel_access_token}'
    }
    try:
        re = http.request('GET', f'https://api-data.line.me/v2/bot/message/{msgId}/content', headers=header)
        with open('tmp.png', 'wb') as f:
            f.write(re.data)
        return True
    except:
        return False
    