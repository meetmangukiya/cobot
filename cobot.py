import json
import requests
import threading
import logging

import sample_script
# Configuration
# -------------

GITHUB_TOKEN = ''
GITTER_TOKEN = ''

ROOMS = [
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
        A dict of room_name as key and room_id as value.
    """
    logging.warn("Running get_room_ids")
    ids = dict()
    for room in rooms:
        rq = requests.get("https://api.gitter.im/v1/rooms", params={'q': room},
                          headers={"Authorization": "Bearer {token}".format(token=GITTER_TOKEN)})
        response = rq.json()
        for i in response["results"]:
            ids[i["name"]] = i['id']
    return ids

def get_messages(id):
    """
    :param id:
        The room ``id`` whose messages have to be retreived via the streaming API.
    :returns:
        A **requests response** object of the keep-alive request for getting
        the messages and the room id.
    """
    logging.warn("Getting messages of id: " + id)
    rq = requests.get("https://stream.gitter.im/v1/rooms/{room_id}/chatMessages".format(room_id=id),
                        stream=True,
                        headers={"Authorization": "Bearer {token}".format(token=GITTER_TOKEN)})
    logging.warn(rq)
    return rq

def listen(regex, handlers=handlers):
    """
    A decorator to add the decorating function as a handler of
    message matching given regex.
    """
    def wrap(func):
        def wrapped(*args, **kwargs):
            logging.warn("Add {}:{} to the handlers".format(regex, func.__name__))
            handlers[regex] = func
            return func(*args)
        return wrapped
    return wrap

def handle_messages(res, id):
    """
    Call the handlers if the message matches the handler's regex.

    :param res:
        The requests response object of a stream api
    """
    logging.warn("Called handle_messages")
    logging.warn(res)
    print(res)
    for msg in res.iter_lines():
        logging.warn(msg)
        if msg:
            logging.warn(msg)
            msg = msg.decode('utf-8')
            logging.warn("msg: " + msg)
            logging.warn("id: " + id)
            for handler in handlers:
                if re.match(handler, msg.text):
                    logging.warn("calling "+ handlers[handler])
                    handlers[handler](msg, id)

def send_message(room_id, msg):
    """
    Send a message to a room

    :param room_id:
        ID of the room to send message to.
    :param msg:
        The message to be sent.
    :returns:
        The response object of the request.
    """
    logging.warn("Sending message: \n\t ", msg, "\n to room ", room_id)
    return requests.post("https://api.gitter.im/v1/rooms/{room_id}/chatMessagges".format(room_id),
                  params={"text": msg})

# Execution
# ---------

if __name__ == "__main__":
    room_ids_dict = get_room_ids(ROOMS)

    threads = []

    for room in room_ids_dict:
        th = threading.Thread(name=room, target=handle_messages,
                              args=get_messages(room_ids_dict[room]),
                              kwargs={"id": room_ids_dict[room]})
        threads.append(th)
        th.start()
