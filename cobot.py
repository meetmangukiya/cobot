import json
import requests

# Configuration
# -------------

GITHUB_TOKEN = ''
GITTER_TOKEN = ''

ROOMS = [
    'coala/coala',
    'coala/cobot-test'
]

# Functionality
# -------------

global handlers
handlers = dict()
def get_room_ids(rooms):
    """
    :pararm rooms:
        List of room names whose room id has to be retreived.
    :return:
        A list of room ids.
    """

    ids = dict()
    for room in rooms:
        rq = requests.get("https://api.gitter.im/v1/rooms?q={room_name}".format(roon_name=room),
                          headers={"Authorization": "Bearer {token}".format(token=GITTER_TOKEN)})
        response = json.loads(rq.json())
        for i in response:
            ids[i.name] = i.id
    return ids

def get_messages(id):
    """
    :param id:
        The room ``id`` whose messages have to be retreived via the streaming API.
    :returns:
        A **requests response** object of the keep-alive request for getting the messages.
    """

    return json.loads(requests.get("https://stream.gitter.im/v1/rooms/{room_id}/chatMessagges".foramt(room_id=id),
                                   stream=True,
                                   headers={"Authorization": "Bearer {token}".format(token=GITTER_TOKEN)}).json())

def listen(regex, handlers=handlers):
    """
    A decorator to add the decorating function as a handler of
    message matching given regex.
    """
    def wrap(func):
        handlers[regex] = func
        func()
    return wrap
