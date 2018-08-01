from django.http import HttpRequest

from connector.consts import mock_channels
from connector.utils import DictResponse


@DictResponse
def list_channels(request: HttpRequest) -> dict:  # pylint: disable=W0613
    '''
    Lists emulated Junebug channels
    '''

    mock_dict = {
        'status': 200,
        'code': 'OK',
        'description': 'channels listed',
        'result': [key for key, value in mock_channels.items()]
    }

    return mock_dict


def get_channel():
    pass


def send_message():
    pass


def chat_send():
    pass
