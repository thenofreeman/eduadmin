from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from eduadmin.auth import login_required
from eduadmin.db import get_db

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    db = get_db()

    return render_template('base.html')