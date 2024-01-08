class User:
    def __init__(self):
        self._holds = []

    def has_holds(self):
        return self._holds