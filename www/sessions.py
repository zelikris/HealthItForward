import json
from datetime import datetime

import base64
import hashlib
import hmac
from flask import g, redirect, url_for, request
from flask.sessions import SessionInterface, SessionMixin
from functools import wraps
from werkzeug.datastructures import CallbackDict


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)

    return wrapper


class JWTSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True

        CallbackDict.__init__(self, initial, on_update)
        self.modified = False


class JWTSessionInterface(SessionInterface):
    class BadTokenException(Exception):
        """Raised when a JWT signature is invalid"""

    @staticmethod
    def jwt_encode(key, claims):
        hmac_maker = hmac.new(key, digestmod=hashlib.sha256)
        header = base64.urlsafe_b64encode('{"typ":"JWT","alg":"HS256"}'.encode('utf-8')).decode('ascii')
        claims = base64.urlsafe_b64encode(json.dumps(claims).encode('utf-8')).decode('ascii')
        payload = header + '.' + claims
        hmac_maker.update(payload.encode('ascii'))
        digest = base64.urlsafe_b64encode(hmac_maker.digest()).decode('ascii')
        return payload + '.' + digest

    @staticmethod
    def jwt_decode(key, encoded):
        header, claims, correct_digest = encoded.split('.')
        payload = header + '.' + claims
        hmac_maker = hmac.new(key, digestmod=hashlib.sha256)
        hmac_maker.update(payload.encode('ascii'))
        digest = base64.urlsafe_b64encode(hmac_maker.digest()).decode('ascii')
        if not hmac.compare_digest(digest, correct_digest):
            raise JWTSessionInterface.BadTokenException()
        claims = base64.urlsafe_b64decode(claims).decode('utf-8')
        return json.loads(claims)

    def open_session(self, app, request):
        if not app.secret_key:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            return JWTSession()
        try:
            session_data = JWTSessionInterface.jwt_decode(app.secret_key, val)
            if session_data.get('iss') != 'ao' or session_data.get('nbf') > int(datetime.utcnow().timestamp()) or \
                    session_data.get('exp') < int(datetime.utcnow().timestamp()):
                raise JWTSessionInterface.BadTokenException()
            return JWTSession(session_data)
        except JWTSessionInterface.BadTokenException:
            return JWTSession()

    def save_session(self, app, session, response):
        if not app.secret_key:
            return

        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        if not session:
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain, path=path)
            return

        httponly = self.get_cookie_httponly(app)
        expires = datetime.utcnow().timestamp() + (app.permanent_session_lifetime if session.permanent else 30 * 60)

        session['exp'] = int(expires)
        if 'nbf' not in session:
            session['nbf'] = int(datetime.utcnow().timestamp())
        if 'iss' not in session:
            session['iss'] = 'ao'

        val = JWTSessionInterface.jwt_encode(app.secret_key, dict(session))
        response.set_cookie(app.session_cookie_name, val, httponly=httponly, expires=expires, domain=domain, path=path,
                            secure=False)
