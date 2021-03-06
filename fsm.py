from linebot.models import (ImageMessage, MessageEvent, StickerMessage,
                            TextMessage, TextSendMessage)
from transitions.extensions import GraphMachine

from imgur import uploadImage
from render import *
from sql import Database
from utils import *

database = Database()

def printState(text):
    print(f'[FSM state] {text}')
class StateMachine(GraphMachine):
    def __init__(self, **mechine_configs):
        self.machine = GraphMachine(
            model = self,
            name='Memecraft State Graph',
            states=['asleep', 'show_temp', 'drake_text_1', 'drake_text_2',
                    'boyfriend_text_1', 'boyfriend_text_2', 'pigeon_text_1',
                    'buttons_text_1', 'buttons_text_2', 'pikachu_text_1',
                    'lotus_1_text_1', 'peony_text_1', 'lotus_2_text_1',
                    'show_blesses', 'show_memes', 'show_result', 'show_usage',
                    'show_gallery', 'show_menu', 'upload_meme', 'get_pic_from_gallery',
                    'show_fsm', 'test_state'],
            initial='asleep',
            transitions=[
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_temp',
                    'conditions': lambda event : event.message.text.lower() in ['templates', '模板']
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'drake_text_1',
                    'conditions': lambda event : event.message.text.lower() == 'drake-approves'
                },
                {
                    'trigger': 'advance',
                    'source': 'drake_text_1',
                    'dest': 'drake_text_2',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'drake_text_2',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'boyfriend_text_1',
                    'conditions': lambda event: event.message.text.lower() == 'distracted-boyfriend'
                },
                {
                    'trigger': 'advance',
                    'source': 'boyfriend_text_1',
                    'dest': 'boyfriend_text_2',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'boyfriend_text_2',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'pigeon_text_1',
                    'conditions': lambda event: event.message.text.lower() == 'is-this-a-pigeon'
                },
                {
                    'trigger': 'advance',
                    'source': 'pigeon_text_1',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'buttons_text_1',
                    'conditions': lambda event: event.message.text.lower() == 'two-buttons'
                },
                {
                    'trigger': 'advance',
                    'source': 'buttons_text_1',
                    'dest': 'buttons_text_2',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'buttons_text_2',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'pikachu_text_1',
                    'conditions': lambda event: event.message.text.lower() == 'surprised-pikachu'
                },
                {
                    'trigger': 'advance',
                    'source': 'pikachu_text_1',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'lotus_1_text_1',
                    'conditions': lambda event: event.message.text.lower() == 'lotus-1'
                },
                {
                    'trigger': 'advance',
                    'source': 'lotus_1_text_1',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'lotus_2_text_1',
                    'conditions': lambda event: event.message.text.lower() == 'lotus-2'
                },
                {
                    'trigger': 'advance',
                    'source': 'lotus_2_text_1',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'peony_text_1',
                    'conditions': lambda event: event.message.text.lower() == 'peony'
                },
                {
                    'trigger': 'advance',
                    'source': 'peony_text_1',
                    'dest': 'show_result',
                    'conditions': 'is_valid_text'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_usage',
                    'conditions': lambda event: event.message.text.lower() in ['usage', '使用說明', '說明']
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_memes',
                    'conditions': lambda event: event.message.text.lower() == 'show_memes'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_blesses',
                    'conditions': lambda event: event.message.text.lower() == 'show_blesses'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'upload_meme',
                    'conditions': lambda event: event.message.text.lower() == 'upload_image'
                },
                {
                    'trigger': 'advance',
                    'source': 'upload_meme',
                    'dest': 'asleep',
                },
                {
                    'trigger': 'image_advance',
                    'source': 'upload_meme',
                    'dest': 'asleep'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'get_pic_from_gallery',
                    'conditions': lambda event: event.message.text[:12].lower() == 'show_gallery'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'test_state',
                    'conditions': lambda event: event.message.text[:5].lower() == 'test_'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_menu',
                    'conditions': lambda event: event.message.text.lower() == 'menu'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_fsm',
                    'conditions': lambda event: event.message.text.lower() == 'fsm'
                },
                {
                    'trigger': 'cancel',
                    'source': ['drake_text_1', 'drake_text_2', 'show_usage', 'show_gallery',
                               'boyfriend_text_1', 'boyfriend_text_2', 'pigeon_text_1',
                               'lotus_1_text_1', 'peony_text_1', 'lotus_2_text_1',
                               'buttons_text_1', 'buttons_text_2', 'pikachu_text_1'],
                    'dest': 'asleep'
                },
                {
                    'trigger': 'go_back',
                    'source': ['drake_text_1', 'drake_text_2', 'show_usage', 'show_gallery',
                               'boyfriend_text_1', 'boyfriend_text_2', 'pigeon_text_1',
                               'lotus_1_text_1', 'peony_text_1', 'lotus_2_text_1',
                               'buttons_text_1', 'buttons_text_2', 'pikachu_text_1',
                               'show_temp', 'show_result', 'show_memes', 'show_blesses',
                               'show_menu', 'get_pic_from_gallery', 'show_fsm', 'test_state'],
                    'dest': 'asleep'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_gallery',
                    'conditions': lambda event: event.message.text.lower() == 'gallery'
                }
            ]
        )

        # use to render text
        self.kind = ''
        self.text_buf = []
        self.gallery_cache = database.getMemesFromGallery()
        self.bless = False

    def is_valid_text(self, event):
        text = event.message.text
        if text != 'cancel' and text != '取消':
            self.text_buf.append(text)
            return True
        else:
            self.cancel()
            return False

    def on_enter_asleep(self, event):
        print('Clear buffer')
        self.kind = ''
        self.text_buf.clear()
        self.bless = False
        return True

    def on_enter_show_temp(self, event):
        reply_token = event.reply_token
        send_templates_menu(reply_token)
        self.go_back(event)

    def on_enter_show_memes(self, event):
        reply_token = event.reply_token
        send_templates(reply_token, 'meme templates', database.getMemes())
        self.go_back(event)

    def on_enter_show_blesses(self, event):
        reply_token = event.reply_token
        send_templates(reply_token, 'bless templates', database.getBlesses())
        self.go_back(event)
    
    def on_enter_show_result(self, event):
        print(f'KIND = {self.kind}')

        link = ''

        if not self.bless:
            # render the picture
            url = database.getURL(self.kind)
            print(f'URL = {url}')
            configs, color, font, fontsize = database.getConfigs(self.kind)
            renderImage(url, self.text_buf, configs, font, fontsize, color)
            link = uploadImage('upload.png', self.kind)
        else:
            url = database.getBlessURL(self.kind)
            print(f'URL = {url}')
            configs, color, outline, font, fontsize = database.getBlessConfigs(self.kind)
            renderImageWithOutline(url, self.text_buf, configs, font, fontsize, color, outline)
            link = uploadImage('upload.png', self.kind)

        # reply the user
        token = event.reply_token
        send_img_message(token, link)

        # upload to gallery
        database.uploadGallery(self.kind, link)

        self.go_back(event)

    def on_enter_drake_text_1(self, event):
        text = event.message.text
        self.kind = text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'Please enter text for top area')

    def on_enter_drake_text_2(self, event):
        text = event.message.text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'Please enter text for bottom area')

    def on_enter_boyfriend_text_1(self, event):
        text = event.message.text
        self.kind = text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'Please enter the left text')

    def on_enter_boyfriend_text_2(self, event):
        text = event.message.text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'Please enter the right text')

    def on_enter_pigeon_text_1(self, event):
        text = event.message.text
        print(f'KIND = {self.kind}')
        self.kind = text

        token = event.reply_token
        send_text_message(token, 'Please enter a text')

    def on_enter_buttons_text_1(self, event):
        text = event.message.text
        self.kind = text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'Please enter text for left button')

    def on_enter_buttons_text_2(self, event):
        text = event.message.text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'Please enter text for right button')

    def on_enter_pikachu_text_1(self, event):
        text = event.message.text
        self.kind = text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'Please enter a message')
    
    def on_enter_lotus_1_text_1(self, event):
        text = event.message.text
        self.kind = text
        self.bless = True
        print(f'KIND = {self.kind}')
        print(f'BLESS = {self.bless}')

        token = event.reply_token
        send_text_message(token, 'Please enter a message')

    def on_enter_lotus_2_text_1(self, event):
        text = event.message.text
        self.kind = text
        self.bless = True
        print(f'KIND = {self.kind}')
        print(f'BLESS = {self.bless}')

        token = event.reply_token
        send_text_message(token, 'Please enter a message')

    def on_enter_peony_text_1(self, event):
        text = event.message.text
        self.kind = text
        self.bless = True
        print(f'KIND = {self.kind}')
        print(f'BLESS = {self.bless}')

        token = event.reply_token
        send_text_message(token, 'Please enter a message')

    def on_enter_upload_meme(self, event):
        token = event.reply_token

        send_text_message(token, 'Please send an image')

    def on_exit_upload_meme(self, event):
        token = event.reply_token

        if isinstance(event.message, TextMessage):
            send_text_message(token, 'Uploading failed')
        if isinstance(event.message, ImageMessage):
            getImageFromLineAPI(event.message.id)
            link = uploadImage('tmp.png', 'user-upload')
            send_text_message(token, 'Uploading succeed')

            database.uploadGallery('user-upload', link)

    def on_enter_show_menu(self, event):
        token = event.reply_token
        send_menu(token)
        self.go_back(event)

    def on_enter_show_usage(self, event):
        token = event.reply_token
        send_usage(token)
        self.go_back(event)
    
    def on_enter_show_gallery(self, event):
        self.gallery_cache = database.getMemesFromGallery()

        token = event.reply_token
        send_gallery(token, self.gallery_cache)
        self.go_back(event)

    def on_enter_get_pic_from_gallery(self, event):
        parsed_text = event.message.text.split('_')
        index = eval(parsed_text[2])

        token = event.reply_token
        url = self.gallery_cache[index][2]
        send_img_message(token, url)

        self.go_back(event)

    def on_enter_test_state(self, event):
        parsed_text = event.message.text.split('_')

        token = event.reply_token
        send_text_message(token, parsed_text[1])
        self.go_back(event)

    def on_enter_show_fsm(self, event):
        token = event.reply_token
        send_img_message(token, 'https://memecraft-bot.herokuapp.com/show_fsm')
        self.go_back(event)
