

class EvtDispatcher:
    def __init__(self):
        self.handlers = {}

    def register(self, evtId, evtHandler):
        self.handlers[evtId] = evtHandler

    def deregister(self, evtId):
        if evtId in self.handlers:
            del self.handlers[evtId]

    def dispatch(self, evtId, content):
        if evtId in self.handlers:
            self.handlers[evtId](content)
            return

evtDispatcher = EvtDispatcher()