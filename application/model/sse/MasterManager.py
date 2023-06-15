import functools
import queue

from application.model.sse.SlaveManager import SlaveManager

# there are flask-sse package, but we need install dependency, and it requires using Redis.
class MasterManager:

    def __init__(self):
        self.slaves = []

    def listen(self,data):
        slave = SlaveManager(data)
        self.slaves.append(slave)
        return slave

    def __str__(self):
        return functools.reduce(lambda x,y : x + str(y) + ',',self.slaves,"[")[:-1] + "]"

    def announce(self, msg):
        for i in reversed(range(len(self.slaves))):
            try:
                self.slaves[i].queueMessage.put_nowait(msg)
            except queue.Full:
                # the slave don't read message, we can considere it as death
                del self.slaves[i]

    # here describe of event structure :
    # https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format
    def format_sse(data: str, event=None) -> str:
        msg = f'data: {data}\n\n'
        if event is not None:
            msg = f'event: {event}\n{msg}'
        return msg
