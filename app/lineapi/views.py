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
from .my_models import regist

def index(request):
    return HttpResponse("This is bot api.")

def callback(request):
    reply = ""
    request_json = json.loads(request.body.decode('utf-8')) # requestの情報をdict形式で取得

    # print(request_json)

    for e in request_json['events']:
        # print(e)
        event_type = e['type']  # Webhookイベント

        # ----------------
        # フォローイベント
        # ----------------
        if event_type == "follow":
            user_id = e['source']['userId']
            reply_token = e['replyToken']  # 返信先トークンの取得

            regist.create_user(user_id)
            reply_text = 'フォローありがとうございます！操作は下のメニューより行ってください。'

            reply += replay.reply_text(reply_token, reply_text)

        # ----------------
        # フォロー解除イベント
        # ----------------
        if event_type == "unfollow":
            user_id = e['source']['userId']

            regist.delete_user(user_id)
            continue

        # ----------------
        # メッセージイベント
        # ----------------
        if event_type == 'message':
            user_id = e['source']['userId']
            text = e['message']['text']    # 受信メッセージの取得
            reply_token = e['replyToken']  # 返信先トークンの取得

            if text.startswith('>get_channels'):
                reply += replay.reply_Youtube(reply_token, user_id)

            # チャンネル登録/削除ボタン
            elif text == '>channnels_regist':
                alt_text = '操作を選択してください'
                buttons = ['>登録','>削除']
                reply += replay.reply_button(reply_token, alt_text, buttons)

            # チャンネル登録:1
            elif text == '>登録':
                reply_text = '登録したいチャンネルURLを入力してください'
                reply += replay.reply_uri(reply_token, reply_text)

            # チャンネル登録:2
            elif text.startswith('https://www.youtube.com/channel/'):
                channel_name = regist.create_channels(reply_token, user_id, text)
                if channel_name:
                    reply_text = '「' + channel_name + '」チャンネルを登録しました！'
                    reply += replay.reply_text(reply_token, reply_text)
                else:
                    reply_text = 'チャンネル登録に失敗しました。\nチャンネルは4件まで登録可能です。'
                    reply += replay.reply_text(reply_token, reply_text)

            # チャンネル削除:1
            elif text == '>削除':
                channels = regist.get_channels(user_id)
                buttons = []
                for channel in channels:
                    item = [channel, channel.getName()]
                    buttons.append(item)

                if buttons:
                    alt_text = '削除を行うチャンネルを選択してください'
                    reply += replay.reply_delbutton(reply_token, alt_text, buttons)
                else:
                    reply_text = '登録されているチャンネルが存在しません。'
                    reply += replay.reply_text(reply_token, reply_text)


            # チャンネル削除:2
            elif text.startswith('del>'):
                result = regist.delete_channels(reply_token, user_id, text)
                if result != 0:
                    reply_text = 'チャンネルを削除しました！'
                    reply += replay.reply_text(reply_token, reply_text)
                else:
                    reply_text = 'チャンネル削除に失敗しました。'
                    reply += replay.reply_text(reply_token, reply_text)

            # 自動返信メッセージ
            else:
                reply_text = '下のメニューボタンから操作を選択してください'
                reply += replay.reply_text(reply_token, reply_text)

    return HttpResponse(reply)
