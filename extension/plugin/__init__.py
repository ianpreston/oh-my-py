class Plugin(object):
    def __init__(self, ipython):
        self.ipython = ipython

    def load(self):
        raise NotImplementedError()
