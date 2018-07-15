"""
The functions.py file includes several functions that are used within the
application.
Functions may be available as a wrapper to be applied at view functions.
"""
import flask
from flask import request, make_response, redirect, flash, json
from functools import wraps
from flask import session as login_session
from app import ADMIN_ID


def login_required(fn):
    """
    Checks if the users login session is set with 'username' to be passed.
    If login session is not correct, the user is redirected to the /login page.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'username' not in login_session:
            flash('Please login to continue', 'warning')
            return redirect('/login')
        else:
            return fn(*args, **kwargs)
    return wrapper


def admin(fn):
    """
    Checks if the user has admin permissions and returns an error message in
    case the user is not.
    Admin users are defined by the GPLUS ID, which has to be set as ADMIN_ID
    in the app.py
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if login_session['gplus_id'] != ADMIN_ID:
            response = make_response(
                json.dumps('Restricted Area. Your ID: '
                           + login_session['gplus_id']), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            return fn(*args, **kwargs)
    return wrapper


def validate_csrf_get(fn):
    """
    Checks for a valid CSRF token for selected GET requests.
    In case the token is not valid the user received an error message.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.args.get('state') != login_session['state']:
            response = make_response(
                json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            return fn(*args, **kwargs)
    return wrapper


def validate_csrf_post(fn):
    """
    Checks for a valid CSRF token for selected POST requests.
    The CSRF token can be set by using the following snippet in your html form:
    "<input type="hidden" name="csrf_token" value="{{ session['state'] }}">"
    In case the token is not valid the user received an error message.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if flask.request.method == 'POST':
            if request.form['csrf_token'] != login_session['state']:
                response = make_response(
                    json.dumps('Invalid state parameter.'), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
            else:
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)
    return wrapper
