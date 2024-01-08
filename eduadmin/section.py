from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from eduadmin.db import get_db

class Section:
    def __init__(self, id):
        self._db = get_db

        self._data = self.db.execute(
            'SELECT * FROM section WHERE section_id = ?', (id,)
        ).fetchone()

        self._id = self._data.section_id
        self._name = self._data.name
        self._desc = self._data.description
        self._registration_capacity = self._data.registration_capacity
        self._waitlist_capacity = self._data.waitlist_capacity

        # TODO: query from db using section-type NOT raw time values in db
        self.important_dates = {
            'registration_opening': '',
            'registration_deadline': '',
            'withdrawal_deadline': '',
        }

        self._roster = self._db.execute(
            'SELECT user_id FROM registration WHERE section_id = ?', (id,)
        ).fetchall()

        self._waitlist = self._db.execute(
            'SELECT user_id FROM waitlist WHERE section_id = ?', (id,)
        ).fetchall()

    def registered_users(self):
        return self._roster

    def waitlisted_users(self):
        return self._waitlist

    def registration_full(self):
        return len(self._roster) >= self._registration_capacity

    def waitlist_full(self):
        return len(self._waitlist) >= self._waitlist_capacity

    def check_condition(self, condition, value):
        match condition:
            case 'registration_full':
                check = self.registration_full()
            case 'waitlist_full':
                check = self.waitlist_full()
            case _:
                pass

        return check == value

    def update(self, action, user_id, time):
        updated = True

        error = None

        match action:
            case 'register':
                try:
                    self._db.execute(
                        'INSERT INTO registration (user_id, section_id, registration_date) VALUES (?, ?)',
                        (user_id, self.id, time)
                    )
                    self._db.commit()
                except self._db.IntegrityError:
                    error = f'User is already registered for this section.'
                else:
                    return redirect(url_for('manage.calendar'))

                flash(error)
            case 'waitlist':
                pass
            case 'deregister' | 'withdrawal':
                pass
            case _:
                updated = False
                pass


        return updated
