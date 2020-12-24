import os

from flask import Flask, request, abort, send_file

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

from fsm import StateMachine
from utils import *

app = Flask(__name__)

machine = StateMachine()

# channel access token
linebot_api = LineBotApi(os.environ.get('LINE_CHANNEL_TOKEN', None))
# channel secret
parser = WebhookParser(os.environ.get('LINE_CHANNEL_SECRET', None))

# listen post request from '/callback'
@app.route('/callback', methods = ['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text = True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        send_usage(event.reply_token)

    return 'OK'

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage) and not isinstance(event.message, ImageMessage):
            continue

        # print(f"REQUEST BODY: \n{body}")

        if isinstance(event.message, ImageMessage):
            # process images
            print('IMAGE ADVANCE')
            res = machine.image_advance(event)
            if res == False:
                send_text_message(event.reply_token, "Not entering any state")
            continue

        if not isinstance(event.message.text, str):
            continue

        try:
            response = machine.advance(event)
            if response == False:
                print("[ERROR] Not entering any State")
                send_menu(event.reply_token)
                
        except:
            print('Error occurs, back to initial state.')
            send_menu(event.reply_token)
            machine.go_back()

        print(f"\nFSM STATE: {machine.state}")

    return "OK"

@app.route('/show_fsm')
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)