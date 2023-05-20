from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.models import *
import openai

import env

line_bot_api = LineBotApi(env.line_access_token)
handler = WebhookHandler(env.line_secrete)
openai.api_key = env.openai_api_key


def reply(event):
    data =event.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"現在你是我的寶貝，請你用情話方式回覆我以下內容，針對訊息回覆就好，越簡短越好:{data}"}
        ]
    ).choices[0].message.content


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )


def song_rec(age, mood):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"請為一位 {age}歲 目前心情 {mood} 的人推薦一首繁體中文歌，請只回覆歌名就好，也不要有歌手"}
        ]
    ).choices[0].message.content

    return response


    