# -*- encoding: utf-8 -*-
import json
import random
import requests
import html
import re

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

from lineapi.models import User,Channels

#LINE
REPLY_ENDPOINT = 'https://api.line.me/v2/bot/message/reply'
HEADER = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + settings.ACCESS_TOKEN
}

# Youtube
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=settings.DEVELOPER_KEY)

# 通常リプライ
def reply_text(reply_token, text):
    payload = {
          "replyToken":reply_token,
          "messages":[
                {
                    "type":"text",
                    "text": text
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return ""

# URIアクション
def reply_uri(reply_token, text):

    # ボタンテンプレート
    template = {
          "type": "buttons",
          "text": "YoutubeからチャンネルURLを共有してください。",
          "actions": [
              {
                  "type": "uri",
                  "label": "Youtubeを開く",
                  "uri": "https://www.youtube.com/"
              }
          ]
    }
    payload = {
          "replyToken": reply_token,
          "messages":[
                {
                    "type": "template",
                    "altText": "YoutubeからチャンネルURLを共有してください。",
                    "template": template
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return ""

# ボタンリプライ
def reply_button(reply_token, alt_text, buttons):
    # ボタンアクション生成
    actions = [] # 初期化
    for i in buttons:
        i = i[:20]
        item = {
            "type": "message",
            "label": i,
            "text": i
        }
        actions.append(item)

    # ボタンテンプレート
    template = {
          "type": "buttons",
          "text": alt_text,
          "actions": actions
    }
    payload = {
          "replyToken": reply_token,
          "messages":[
                {
                    "type": "template",
                    "altText": alt_text,
                    "template": template
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return ""


# 削除用ボタンリプライ
def reply_delbutton(reply_token, alt_text, buttons):
    # ボタンアクション生成
    actions = [] # 初期化
    for i in buttons:
        id = str(i[0])
        name = i[1]

        name = name[:20]
        item = {
            "type": "message",
            "label": name,
            "text": 'del>' + id
        }
        actions.append(item)

    # ボタンテンプレート
    template = {
          "type": "buttons",
          "text": alt_text,
          "actions": actions
    }
    payload = {
          "replyToken": reply_token,
          "messages":[
                {
                    "type": "template",
                    "altText": alt_text,
                    "template": template
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return ""

# 3-1 動画一覧表示
def reply_Youtube(reply_token, user_id):

    user = User.objects.get(user_id=user_id)
    channels = user.channels_set.all() # チャンネルID逆参照


    # チャンネルIDセット
    channels_ids = []
    for channel in channels:
        channels_ids.append(str(channel))
    channels_id = ','.join(channels_ids)

    # チャンネル取得
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channels_id
    ).execute()
    channel_items = channel_response.get("items", [])

    # チャンネルごとの動画抽出
    messages = []
    for c in channel_items:
        videos = []
        channel_id = c['id']

        search_response = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=5,
            order="date"
        ).execute()
        search_items = search_response.get("items", [])
        videos.append(search_items)

        # columns取得
        columns = get_columns(videos)

        template = {
            "type": "carousel",
            "columns": columns
        }
        message = {
            "type":"template",
            "altText": "this is a carousel template",
            "template": template
        }
        messages.append(message)


    payload = {
      "replyToken":reply_token,
      "messages": messages
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return ""

# 3-2 カラム取得
def get_columns(videos):
    columns = []
    for video in videos:
        for v in video:

            # サムネイル
            image = html.escape(v['snippet']['thumbnails']['medium']['url'])
            # タイトル
            title = v['snippet']['title']
            title = title[:40]
            # 説明文
            description = v['snippet']['description']
            description = description[:60]

            # columns組み立て
            col = {
                "thumbnailImageUrl": image,
                "imageBackgroundColor": "#000000",
                "title": title,
                "text": description,
                "defaultAction": {
                    "type": "uri",
                    "label": "View detail",
                    "uri": "http://example.com/page/123"
                },
                "actions": [
                    {
                        "type": "uri",
                        "label": "Youtube",
                        "uri": "https://www.youtube.com/watch?v="+v['id']['videoId']
                    }
                ]
              }
            columns.append(col)

    return columns
