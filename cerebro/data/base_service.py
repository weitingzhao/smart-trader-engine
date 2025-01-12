from .progress import Progress


class BaseService():

    def __init__(self):
        self.progress = Progress()
