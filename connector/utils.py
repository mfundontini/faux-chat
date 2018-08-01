from json import dumps

from functools import wraps
from typing import Any, Callable

from django.http import HttpRequest, HttpResponse


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
