# -*- coding: utf-8 -*-

import requests

def post_message(token, channel, text):
    requests.post("https://slack.com/api/chat.postMessage",
                     headers={"Authorization": "Bearer " + token},
                     data={"channel": channel, "text": text}
                     )
    print('chat_write완료 ',text)