import requests

from uuid import uuid4
from json import dumps, loads

from django.http import HttpRequest
from django.utils import timezone

from connector.consts import MOCK_CHANNELS
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
        'result': [key for key, value in MOCK_CHANNELS.items()]
    }

    return mock_dict


@DictResponse
def get_channel(request: HttpRequest, cid: str) -> dict:
    '''
    Returns config for the mock channels
    '''
    chn = MOCK_CHANNELS.get(cid)
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
    channel = MOCK_CHANNELS.get(cid)

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
    print(type(data))

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


@DictPostResponse
def chat_send(request: HttpRequest, cid: str) -> dict:
    '''
    Send chat message
    '''

    channel = MOCK_CHANNELS.get(cid)
    channel_data = {
        'session_event': 'resume',
    }  # type: dict

    data = request.json.get('data', {})
    if data:
        if channel['type'] == 'facebook':
            channel_data['messenger'] = loads(data['payload'])
        elif channel['type'] == 'telegram':
            channel_data['telegram'] = {
                'reply': data['payload']
            }
        content = data.get('title', '')
    else:
        content = request.json.get('content', '')

    # record_messages(request, cid, [{'user': True, 'content': content}])

    requests.post(
        channel['mo_url'],
        json={
            'channel_data': channel_data,
            'from': request.json['address'],
            'channel_id': channel['id'],
            'timestamp': str(timezone.now()),
            'content': request.json['content'],
            'to': channel['id'],
            'reply_to': None,
            'message_id': str(uuid4())
        }
    )

    return {
        'status': 'ok'
    }

