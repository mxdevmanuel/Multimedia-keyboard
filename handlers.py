import pyinotify


class WatchEventHandler(pyinotify.ProcessEvent):

    def __init__(self, queue):
        self.queue = queue
        super(WatchEventHandler, self).__init__()

    def process_IN_CREATE(self, event):
        print('Running: ', event.pathname)
        if self.queue.full():
            self.queue.get()
        self.queue.put(True)

    def process_IN_DELETE(self, event):
        print("Stopped: ", event.pathname)
        if self.queue.full():
            self.queue.get()
        self.queue.put(False)
