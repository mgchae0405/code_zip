# -*- coding: utf-8 -*-

from slack import WebClient

def post_image(token, channel, filepath):
    client = WebClient(token=token)
    client.files_upload(channels=channel, file=filepath)
    print('file_write완료')
