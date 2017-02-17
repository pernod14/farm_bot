# -*- encoding: utf-8 -*-
import json
import random
import requests

from django.shortcuts import render
from django.http import HttpResponse

import sys
sys.path.append('bot/')
from load_serif import councelor_serif

REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
ACCESS_TOKEN = 'fUCIabgTmtHFLi+yf/BTibQoL/UbPgkHH9GUUNpeYuExj+2d0NOt8fCwIDa+aNDSbVnaEwlm1ZGTTFikmNlyZES5woCL5RGDxqdz+VhAJorokEUhrCGUEQ8++LtyqmBX85BWsUHPQpEmcp/jCEp3DgdB04t89/1O/w1cDnyilFU='
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
}

def index(request):
    return HttpResponse("This is bot api desu.")

def reply_text(reply_token, text):
    #reply = random.choice(councelor_serif)
    reply = chose_serif(text, councelor_serif)
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": reply
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return reply

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # typeの取得

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得
            reply += reply_text(reply_token, text)   # LINEにセリフを送信する関数
        else:
            reply += reply_text(reply_token, "photo")
    return HttpResponse(reply)  # テスト用


def chose_serif(text, councelor_serif):
    text = text.lower()
    if "hajimaru" in text:
        return "Sounds good! Where is?"
    elif "tokyo" in text:
        return "City farmer! What's your recommend?"
    elif "tomato" in text or "potato" in text or "pumpkin" in text:
        return "I like it! Show me the photo!"
    elif "photo" in text:
        return "Lovely! Nice photo! Finally, tell me your farm concept."
    elif "bootstrap" in text:
        return "Touching! How about this one. http://hajimaru-farm00.herokuapp.com"
    else:
        return "OMG! It's out of scenario. Tell me your farm name again!"
