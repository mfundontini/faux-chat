from connector.consts import MOCK_CHANNELS


def get_channels(request):
    return {
        "get_channels": [
            {"id": channel, "label": data["label"]
             } for channel, data in MOCK_CHANNELS.items()]
    }
