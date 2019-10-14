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

# チャンネルリスト
channels_list = {
  "本間ひまわり": "UC0g1AE0DOjBYnLhkgoRWN1w",
  "アンジュ・カトリーナ": "UCHVXbQzkl3rDfsXWo8xi2qw",
  "リゼ・ヘルエスタ": "UCZ1xuCK1kNmn5RzPYIZop3w",
  "笹木咲": "UCoztvTULBYd3WmStqYeoHcA"
}

# 通常リプライ
def reply_text(reply_token, text):
    replybox = ['毎日勉強！','頑張る！','レベルの高い大学に行くんだ！']
    reply = random.choice(replybox)
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

# 登録済みチャンネル一覧をリプライ
def reply_channel(reply_token, text):
    # ボタンテンプレート
    template = {
          "type": "buttons",
          "text": "「にじさんじ」に所属するチャンネル一覧",
          "actions": [
              {
                  "type": "message",
                  "label": "本間ひまわり",
                  "text": ">channels: 本間ひまわり"
              },
              {
                  "type": "message",
                  "label": "アンジュ・カトリーナ",
                  "text": ">channels: アンジュ・カトリーナ"
              },
              {
                  "type": "message",
                  "label": "リゼ・ヘルエスタ",
                  "text": ">channels: リゼ・ヘルエスタ"
              },
              {
                  "type": "message",
                  "label": "笹木咲",
                  "text": ">channels: 笹木咲"
              },
          ]
      }
    payload = {
          "replyToken": reply_token,
          "messages":[
                {
                    "type": "template",
                    "altText": "にじさんじに所属するチャンネル一覧",
                    "template": template
                }
            ]
    }

    requests.post(REPLY_ENDPOINT, headers=HEADER, data=json.dumps(payload)) # LINEにデータを送信
    return ""


    # 3-1 動画一覧表示
    def reply_Youtube(reply_token, text):

        # チャンネルIDセット
        get_text = text.replace('>channels: ', '')
        select_channel_id = channels_list[get_text]

        # チャンネル取得
        channel_response = youtube.channels().list(
            part="contentDetails",
            id=select_channel_id
            ).execute()
        channel_items = channel_response.get("items", [])

        # チャンネルごとの動画抽出
        videos = []
        for c in channel_items:
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
        payload = {
              "replyToken":reply_token,
              "messages":[
                    {
                        "type":"template",
                        "altText": "this is a carousel template",
                        "template": template
                    }
                ]
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
