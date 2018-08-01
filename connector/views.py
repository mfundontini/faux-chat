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


@DictResponse
def get_channel(request: HttpRequest, cid: str) -> dict:
    '''
    Returns config for emulated Junebug cid channel
    '''
    chn = mock_channels.get(cid)
    return {
        'status': 200,
        'code': 'OK',
        'description': 'channel found',
        'result': {
            'label': chn['label'],
            'type': chn['type'],
            'mo_url': chn['mo_url'],
            'id': cid,
            'config': chn['config'],
            'metadata': chn['metadata'],
            'view_url': chn['view_url'],
        }
    }


def send_message():
    pass


def chat_send():
    pass
