import pytest

from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.testing import HttpCommunicator, WebsocketCommunicator
from django.conf.urls import url

from chatpaa.consumers import ChatConsumer

@pytest.mark.asyncio
async def test_chat_consumer():
    application = URLRouter([
        url(r'ws/chatpaa/(?P<room_name>\w+)/$', ChatConsumer),
    ])
    communicator = WebsocketCommunicator(application, '/ws/chatpaa/room_1/')
    connected, subprotocol = await communicator.connect()
    assert connected
    response = await communicator.receive_json_from()
    assert response['message'] == '# ws connection established'
    await communicator.send_json_to({
                'type': 'chat_message',
                'message': 'hello'
            }
    )
    response = await communicator.receive_json_from()
    assert response['message'] == 'hello'

    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        'chat_room_1',
        {
            'type': 'chat_message',
            'message': 'hi',
        },
    )
    response = await communicator.receive_json_from()
    assert response['message'] == 'hi'

    await communicator.disconnect()