from transitions.extensions import GraphMachine
from utils import *

from sql import Database
from render import renderImage
from imgur import uploadImage

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, StickerMessage
)

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
                    'two-buttons', 'pikachu', 'show_result', 'show_usage', 'test'],
            initial='asleep',
            transitions=[
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'show_temp',
                    'conditions': lambda event : event.message.text.lower() == 'templates'
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
                    'conditions': lambda event: event.message.text == 'distracted-boyfriend'
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
                    'conditions': lambda event: event.message.text == 'is-this-a-pigeon'
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
                    'dest': 'show_usage',
                    'conditions': lambda event: event.message.text in ['usage', '使用說明']
                },
                {
                    'trigger': 'cancel',
                    'source': ['drake_text_1', 'drake_text_2', 'boyfriend_text_1', 'boyfriend_text_2',
                               'pigeon_text_1', 'distracted', 'pigeon', 'two-buttons', 'pikachu'],
                    'dest': 'asleep'
                },
                {
                    'trigger': 'go_back',
                    'source': ['asleep', 'show_temp', 'drake_text_1', 'drake_text_2',
                               'boyfriend_text_1', 'boyfriend_text_2', 'pigeon_text_1',
                               'two-buttons', 'pikachu', 'show_result', 'show_usage', 'test'],
                    'dest': 'asleep'
                },
                {
                    'trigger': 'advance',
                    'source': 'asleep',
                    'dest': 'test',
                    'conditions': lambda event: event.message.text == 'test'
                }
            ]
        )

        # use to render text
        self.kind = ''
        self.text_buf = []

    def is_valid_text(self, event):
        text = event.message.text
        if text != 'cancel' and text != '取消':
            self.text_buf.append(text)
            return True
        else:
            self.cancel()
            return False

    def on_enter_asleep(self):
        print('Clear buffer')
        self.kind = ''
        self.text_buf.clear()
        return True

    def on_enter_show_temp(self, event):
        reply_token = event.reply_token
        send_templates(reply_token, 'meme templates', database.getMemes())
        self.go_back()
    
    def on_enter_show_result(self, event):
        print(f'KIND = {self.kind}')

        # render the picture
        url = database.getURL(self.kind)
        print(f'URL = {url}')
        configs, color, font, fontsize = database.getConfigs(self.kind)
        renderImage(url, self.text_buf, configs, font, fontsize, color)
        link = uploadImage('upload.png', self.kind)

        # reply the user
        token = event.reply_token
        send_img_message(token, link)

        # upload to gallery
        database.uploadGallery(self.kind, link)

        self.go_back()
        return 'OK'

    def on_enter_drake_text_1(self, event):
        text = event.message.text
        self.kind = text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'the first text')

    def on_enter_drake_text_2(self, event):
        text = event.message.text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'the second text')

    def on_enter_boyfriend_text_1(self, event):
        text = event.message.text
        self.kind = text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'the first text')

    def on_enter_boyfriend_text_2(self, event):
        text = event.message.text
        print(f'KIND = {self.kind}')

        token = event.reply_token
        send_text_message(token, 'the second text')

    def on_enter_pigeon_text_1(self, event):
        text = event.message.text
        print(f'KIND = {self.kind}')
        self.kind = text

        token = event.reply_token
        send_text_message(token, 'enter the text')

    def on_enter_show_usage(self, event):
        token = event.reply_token
        send_usage(token)
        self.go_back()
    
    def on_enter_test(self, event):
        memes = database.getMemesFromGallery()

        token = event.reply_token
        send_gallery(token, memes)
        self.go_back()