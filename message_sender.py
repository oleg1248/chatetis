import os
import time
from random import randint

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatetis.settings')
channel_layer = get_channel_layer()

while True:
    async_to_sync(channel_layer.group_send)(
        'chat_Lobby',
        {
            'type': 'chat_message',
            'message': 'hello world' + str(randint(0, 1000000)),
        },
    )
    time.sleep(1)

print('done')

