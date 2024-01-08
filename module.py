from userlist import UserList

class Module:
    def __init__(self):
        self.important_dates = {
            'registration_opening': '',
            'registration_deadline': '',
            'withdrawal_deadline': '',
        }

        self._roster = UserList()
        self._waitlist = UserList()

    def registered_users(self):
        return self._roster.users

    def waitlisted_users(self):
        return self._waitlist.users

    def registration_full(self):
        return self._roster.is_full

    def waitlist_full(self):
        return self._waitlist.is_full

    def update(self, action, user_id, time):
        updated = True

        match action:
            case 'register':
                # updated = db[courses].addentry(user_id, time)
                pass
            case 'waitlist':
                pass
            case 'deregister' | 'withdrawal':
                pass
            case _:
                updated = False
                pass

        return updated
