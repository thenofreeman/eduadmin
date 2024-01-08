class UserList:
    def __init__(self):
        self._count = 0
        self._capacity = 0

    def is_full(self):
        return self._count >= self._capacity

    def users(self):
        pass # query db for users
