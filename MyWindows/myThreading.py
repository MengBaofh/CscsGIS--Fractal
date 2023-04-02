from threading import *


class AnalyseThread(Thread):
    def __init__(self, group=None, target=None, name='AnalyseThread', args=(), kwargs=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=True)
        self.group = group
        self.target = target
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.daemon = True
