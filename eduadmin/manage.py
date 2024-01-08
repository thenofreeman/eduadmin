import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from module import Module
from user import User

bp = Blueprint('manage', __name__, url_prefix='/manage')

@bp.post('/register')
def register(module_id, user_id):
    module = Module[module_id]

    conditions = [{
        'condition': module.registration_full, 
        'message': 'Registration is full.'
    }]

    response = update_module(module_id=module_id, 
                            user_id=user_id, 
                            action='register',
                            conditions=conditions,
                            opening='registration_opening', 
                            closing='registration_deadline')

    return response

@bp.post('/waitlist')
def waitlist(module_id, user_id):
    module = Module[module_id]

    conditions = [{
        'condition': module.registration_full, 
        'message': 'Registration is full.'
    }, {
        'condition': module.waitlist_full,
        'message': 'Waitlist is full.'
    }]

    response = update_module(module_id=module_id, 
                            user_id=user_id, 
                            action='waitlist',
                            conditions=conditions,
                            opening='registration_opening', 
                            closing='registration_deadline')

    return response

@bp.post('/deregister')
def deregister(module_id, user_id):
    response = update_module(module_id=module_id, 
                            user_id=user_id, 
                            action='deregister',
                            opening='registration_opening',
                            closing='registration_deadline')

    return response

@bp.post('/withdrawal')
def withdrawal(module_id, user_id):
    response = update_module(module_id=module_id, 
                            user_id=user_id, 
                            action='withdrawal',
                            opening='registration_deadline', 
                            closing='withdrawal_deadline')

    return response

def update_module(module_id, user_id, action, conditions, opening, closing):
    user = User(user_id)
    module = Module(module_id)

    responses = []

    attempt_time = time.now()

    for condition in conditions:
        if not condition.condition:
            responses.append((False, f'{condition.message}'))

    if attempt_time < module.important_dates[opening]:
        responses.append((False, f'Attempting to {action} before period is open.'))

    if attempt_time >= module.important_dates[closing]:
        responses.append((False, f'Exceeded deadline to {action}.'))

    if user.has_holds:
        responses.append((False, 'User has holds.'))


    successes, messages = zip((success, message) for success, message in responses)

    response = { 
        'success': all(successes),
        'message': 'Updated successfully.'
    }

    if response.success:
        if not module.update(action, user_id, attempt_time):
            response.success = False
            response.message = f'Database failure.'

    else:
        response.message = '\n'.join(message for message in messages)

    return response