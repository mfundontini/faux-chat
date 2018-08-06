from json import dumps, loads
from uuid import uuid4
import html
import requests

from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from emoji import Emoji  #

from chat.models import Chat
from connector.consts import CHANNEL


def DictResponse(callback: Callable) -> Callable:  # pylint: disable=C0103
    '''
    Wraps the Django view to recieve data as JSON,
     and if you return a dict it is auto-converted to JSON as well
    '''
    @wraps(callback)
    def wrapper(*args: Any, **kwargs: Any) -> HttpResponse:  # pylint: disable=C0111
        request = args[0]  # type: HttpRequest

        # Want error messages in json
        request.content_type = 'application/json'

        result = callback(*args, **kwargs)
        if isinstance(result, HttpResponse):  # pragma: nocoverage
            return result

        resp = HttpResponse(
            dumps(result),
            content_type='application/json',
        )
        resp['Cache-Control'] = 'no-store'
        resp['Pragma'] = 'no-cache'
        return resp

    return wrapper


def DictPostResponse(callback: Callable) -> Callable:  # pylint: disable=C0103
    '''
    Wraps the Django view to recieve data as JSON,
     and if you return a dict it is auto-converted to JSON as well
    '''
    @wraps(callback)
    @csrf_exempt
    @require_POST
    def wrapper(*args: Any, **kwargs: Any) -> HttpResponse:  # pylint: disable=C0111
        request = args[0]  # type: HttpRequest

        # Want error messages in json
        request.content_type = 'application/json'
        try:
            request.json = loads(request.body)
        except ValueError:  # pragma: nocoverage
            return HttpResponse(
                '{"status":"error","reason":"JSON payload_expected"}',
                status=400,
                content_type='application/json',
            )

        result = callback(*args, **kwargs)
        if isinstance(result, HttpResponse):  # pragma: nocoverage
            return result

        sval = 400 if result.get('status') == 'error' else 200
        resp = HttpResponse(
            dumps(result),
            status=sval,
            content_type='application/json',
        )
        resp['Cache-Control'] = 'no-store'
        resp['Pragma'] = 'no-cache'
        return resp

    return wrapper


def post_to_feersum(data: dict, instance: Any):
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


def escape_message(dat: dict) -> None:
    '''
    Escapes message for safe rendering
    '''
    if 'title' in dat:
        if dat['title'] is None:
            del dat['title']
        else:
            dat['title'] = Emoji.replace_unicode(html.escape(dat['title']))
    if 'content' in dat:
        if dat['content'] is None:
            del dat['content']
        else:
            if dat.get('parse_mode') == 'html':
                dat['content'] = Emoji.replace_unicode(dat['content'])
            else:
                dat['content'] = Emoji.replace_unicode(html.escape(dat['content']))
    for btn in dat.get('buttons', []):
        try:
            btn['data']['title'] = Emoji.replace_unicode(html.escape(btn['data']['title']))
        except KeyError:
            pass
    for btn in dat.get('quick_replies', []):
        try:
            btn['title'] = Emoji.replace_unicode(html.escape(btn['title']))
        except KeyError:  # pragma: nocoverage
            pass


def save_feersum_message(data: dict):
    pages = data.get('content', {}).get('channel_data', {}).get('pages', [])

    if pages:
        for page in pages:
            title = page.get('title')
            content = page['text']
            if page.get('buttons'):
                for btn in page.get('buttons'):
                    content += f"\n{btn.get('text')}"
            obj = {
                "title": title,
                "content": content,
                "send_to": CHANNEL,
                "address": "Feersum",
                "channel": CHANNEL,
                "uid": str(uuid4())
            }
            instance = Chat(**obj)
            instance.save()
