from uuid import uuid4
from json import dumps

from django.http import HttpRequest
from django.utils import timezone

from connector.consts import mock_channels
from connector.utils import DictResponse, DictPostResponse, escape_message


@DictResponse
def list_channels(request: HttpRequest) -> dict:  # pylint: disable=W0613
    '''
    Lists mock channels
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
    Returns config for the mock channels
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
            'view_url': chn.get('view_url'),
        }
    }


@DictPostResponse
def receive_message(request: HttpRequest, cid: str) -> dict:
    '''
    Receives messages from feersum
    '''
    channel = mock_channels.get(cid)

    if channel['type'] in ['plaintext', 'twitter']:
        data = {'content': request.json['content']}

    elif channel['type'] == 'facebook':
        pass

    elif channel['type'] == 'telegram':
        pass

    else:  # pragma: nocoverage
        data = {'content': dumps(request.json)}

    # Replace unicode emojis
    if 'list' in data:
        for ldat in data['list']:
            escape_message(ldat)
    elif 'carousel' in data:
        for ldat in data['carousel']:
            escape_message(ldat)
    else:
        escape_message(data)
    print(data)

    # queue_message(request.json['to'], data)

    # TODO: Emulate message status
    return {
        'code': 'OK',
        'status': 200,
        'result': {
            'message_id': str(uuid4()),
            'timestamp': str(timezone.now()),  # Naive timestamp as per JB
            'channel_id': cid
        },
        'description': 'message received'
    }


def chat_send():
    pass
