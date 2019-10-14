# -*- encoding: utf-8 -*-
import json
import random
import requests
import html
import re

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from .my_models import replay

def index(request):
    return HttpResponse("This is bot api.")


def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得
    for e in request_json['events']:
        reply_token = e['replyToken']  # 返信先トークンの取得
        message_type = e['message']['type']   # メッセージtypeの取得

        # print(e)

        if message_type == 'text':
            text = e['message']['text']    # 受信メッセージの取得

            if text.startswith('>channels: '):
                reply += replay.reply_Youtube(reply_token, text)
            elif text == 'にじさんじ':
                reply += replay.reply_channel(reply_token, text)
            elif text == '>channnels_regist':
                # チャンネル登録
                reply += replay.reply_channel(reply_token, text)
            else:
                reply += replay.reply_text(reply_token, text)
    return HttpResponse(reply)
