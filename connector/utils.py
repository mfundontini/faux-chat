from json import dumps, loads
import html

from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from emoji import Emoji  #


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
