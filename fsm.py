from transitions.extensions import GraphMachine
from utils import *

from sql import Database

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
                    'distracted', 'pigeon', 'two-buttons', 'pikachu', 'show_result'],
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
                    'conditions': lambda event : event.message.text.lower() == 'drake-appoves'
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
                    'trigger': 'cancel',
                    'source': ['show_temp', 'drake_text_1', 'drake_text_2', 'distracted', 'pigeon', 'two-buttons', 'pikachu'],
                    'dest': 'asleep'
                },
                {
                    'trigger': 'go_back',
                    'source': ['show_temp', 'drake', 'distracted', 'pigeon', 'two-buttons', 'pikachu', 'show_result'],
                    'dest': 'asleep'
                }
            ]
        )

    def is_valid_text(self, event):
        text = event.message.text
        if text != 'cancel' and text != '取消':
            return True
        else:
            self.cancel()
            return False

    def is_going_to_show_temp(self, event):
        print('Enter show_temp')
        text = event.message.text
        return text.lower() == "template"

    def on_enter_show_temp(self, event):
        reply_token = event.reply_token
        send_templates(reply_token, 'meme templates', database.getMemes())
        self.go_back()

    def is_going_to_drake(self, event):
        text = event.message.text
        return text.lower() == "drake-appoves"
    
    def on_enter_show_result(self, event):
        token = event.reply_token
        send_text_message(token, 'back to asleep')
        self.go_back()
        return 'OK'
