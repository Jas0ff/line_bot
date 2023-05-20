from flask import Flask, request, abort, send_file

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


import ngrok
import json
import os

import env
import custom_msg
import db
import ai
import song

port = 5000
app = Flask(__name__)

line_bot_api = LineBotApi(env.line_access_token)
handler = WebhookHandler(env.line_secrete)

@app.route('/')
def home():
    return '<h1>Test<h1>'

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('無效的token')
        abort(400)
    
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userid = json.loads(str(event))['source']['userId']

    if not db.user_exists(userid):
        line_bot_api.reply_message(
            event.reply_token,
            custom_msg.method_choose
        )
        return 
    
    status = db.get_user_status(userid)
    if status == 'aichat':
        ai.reply(event)


@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    userid = json.loads(str(event))['source']['userId']

    if not db.user_exists(userid):
        line_bot_api.reply_message(
            event.reply_token,
            custom_msg.method_choose
        )
        return 
    
    status = db.get_user_status(userid)
    if status == 'moodsong':
        message_id = event.message.id
        message_content = line_bot_api.get_message_content(message_id)
        image_data = message_content.content
        age, mood = song.recognize_mood(image_data)
        song.reply(event, age, mood)
        if os.path.exists(str(env.temp_dir)+'\\temp.png'):
            os.remove(str(env.temp_dir)+'\\temp.png')


@handler.add(PostbackEvent)
def handle_postback(event):
    userid = json.loads(str(event))['source']['userId']
    if db.user_exists(userid):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="你已經選過了，叫上你的朋友一起試吧!")
        )
        return 
        
    user_choose = event.postback.data
    db.add_user(userid, user_choose)

    if user_choose == 'lottery':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="祝您中獎")
        )
    elif user_choose == 'aichat':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您的小寶貝已上線")
        )
    elif user_choose == 'moodsong':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請自拍或上傳一張照片以偵測您的心情")
        )


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        custom_msg.method_choose
    )
    

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    userid = json.loads(str(event))['source']['userId']
    db.delete_user(userid)



@app.route('/get_img')
def handle_img():
    return send_file(str(env.temp_dir)+'\\temp.png', mimetype='image/png')


def unlink_user(user_id):
    line_bot_api.unlink_rich_menu_from_user(user_id)

if __name__ == '__main__':
    tunnel = ngrok.connect(port, authtoken=env.ngrok_auth)
    print(f'entry at: {tunnel.url()}')
    env.website_url = tunnel.url()
    app.run(port=port)
    