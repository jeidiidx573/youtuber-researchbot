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

# ユーザー登録
def create_user(user_id):
    db = User(
        user_id = user_id
    )
    db.save()
    # result = User.objects.all()

    return ""

# ユーザー削除
def delete_user(user_id):
    user = User.objects.filter(user_id=user_id)
    user.delete()

    # result = User.objects.all()

    return ""

# Youtubeチャンネル登録
def create_channels(reply_token, user_id, text):
    user = User.objects.get(user_id=user_id)

    # チャンネルID取得
    get_id = text.replace('https://www.youtube.com/channel/', '')
    select_channel_id = get_id

    # チャンネル取得
    channel_response = youtube.channels().list(
        part="snippet",
        id=select_channel_id
    ).execute()
    channel_items = channel_response.get("items", [])

    db = Channels(
        user = user,
        channel_id = channel_items[0]['id'],
        channel_name = channel_items[0]['snippet']['title']
    )
    db.save()

    return ""
