from __future__ import absolute_import, unicode_literals

import json
import requests
from celery import shared_task
from typing import Any


@shared_task(ignore_result=True)
def async_post_to_feersum(data: dict, instance: Any):
    instance = json.loads(instance)
    url = data["mo_url"]
    channel = data["id"]

    try:
        res = requests.post(
            url=url,
            json={
                'channel_data': {
                    'session_event': 'resume'
                },
                'from': instance.address,
                'channel_id': channel,
                'timestamp': str(instance.timestamp),
                'content': instance.content,
                'to': channel,
                'reply_to': None,
                'message_id': instance.uid
            }
        )
    except Exception as ex:
        print(str(ex))
    else:
        print(f"INFO: Sent to: {url} with status code: {res.status_code} - {res.reason}")