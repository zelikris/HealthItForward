import datetime
import uuid
from binascii import unhexlify, hexlify
from urllib.parse import urljoin, parse_qs, urlencode

import config
import const
import db
import pbkdf2
import sessions
import hmac
import hashlib
import base64
from flask import Flask, render_template, request, session, g, redirect, url_for, flash, abort
from htmlmin.main import minify

app = Flask(__name__)
app.secret_key = unhexlify('e3d7f0871b236241be434fe4cc789f2e72b970b5a13502488a2d259574911b65')
app.session_interface = sessions.JWTSessionInterface()
app.debug = True


@app.before_request
def before_request():
    g.user = None
    if 'sub' in session:
        g.user = db.session.query(db.User).filter_by(email=session['sub']).one_or_none()


@app.after_request
def response_minify(response):
    if not app.debug and response.content_type == u'text/html; charset=utf-8':
        response.set_data(minify(response.get_data(as_text=True)))
    return response


@app.teardown_appcontext
def teardown_db_session(exception=None):
    db.session.remove()


@app.context_processor
def inject_template_data():
    return dict(const=const, user=g.user, discourse_url=config.discourse_url)


@app.route('/profile')
@sessions.login_required
def profile():
    return redirect(url_for('index_page'))  # TODO


@app.route('/surveys')
@sessions.login_required
def surveys_page():
    return render_template('surveys.html')


@app.route('/logout')
@sessions.login_required
def logout():
    session.clear()
    return redirect(url_for('index_page'))


@app.route('/discourse/login')
@sessions.login_required
def discourse_login():
    if 'sso' not in request.args:
        return redirect(urljoin(config.discourse_url, '/login'))
    h = hmac.new(config.discourse_sso_secret.encode('utf-8'), request.args['sso'].encode('utf-8'), hashlib.sha256)
    digest = h.digest()
    given = unhexlify(request.args['sig'])
    if not hmac.compare_digest(digest, given):
        abort(403)
    payload = base64.b64decode(request.args['sso'])
    payload = parse_qs(payload.decode('utf-8'))
    payload = {'nonce': payload['nonce']}
    payload['email'] = g.user.email
    payload['require_activation'] = 'true'
    payload['external_id'] = g.user.id
    payload['username'] = g.user.screen_name
    payload = urlencode(payload, doseq=True)
    payload = base64.b64encode(payload.encode('utf-8'))
    h = hmac.new(config.discourse_sso_secret.encode('utf-8'), payload, hashlib.sha256)
    payload = payload.decode('utf-8')
    digest = hexlify(h.digest()).decode('utf-8')
    return redirect(urljoin(config.discourse_url, '/session/sso_login?sso={0}&sig={1}'.format(payload, digest)))


@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user = db.session.query(db.User).filter_by(email=request.form['email']).one_or_none()
    password_hash = user.password_hash if user is not None else pbkdf2.fake_digest()
    ok = pbkdf2.verify(request.form['password'], password_hash)
    if ok:
        session['sub'] = request.form['email']
        next = request.args.get('next') or '/profile'
        return redirect(urljoin(request.url_root, next))
    else:
        flash(u'Invalid username or password.', 'danger')
        return login_page()


@app.route('/register', methods=['GET'])
def register_page(formdata=None):
    return render_template('register.html', formdata=formdata)


@app.route('/register', methods=['POST'])
def register():
    for field in ['name', 'email', 'password', 'confirmpassword', 'dob', 'country', 'sex']:
        if field not in request.form or not request.form[field]:
            flash(u'All fields are required.', 'danger')
            return register_page(formdata=request.form)
    if 'terms' not in request.form:
        flash(u'You must accept the terms and conditions.', 'danger')
        return register_page(formdata=request.form)
    if request.form['password'] != request.form['confirmpassword']:
        flash(u'The two passwords did not match.', 'danger')
        return register_page(formdata=request.form)
    if '@' not in request.form['email']:
        flash(u'Invalid email address.', 'danger')
        return register_page(formdata=request.form)
    if request.form['country'] not in const.country_codes:
        flash(u'Invalid country.', 'danger')
        return register_page(formdata=request.form)
    if request.form['sex'] not in const.sex_codes:
        flash(u'Invalid sex.', 'danger')
        return register_page(formdata=request.form)
    try:
        datetime.datetime.strptime(request.form['dob'], '%Y-%m-%d')
    except ValueError:
        flash(u'Invalid birth date.', 'danger')
        return register_page(formdata=request.form)

    user = db.session.query(db.User).filter_by(email=request.form['email']).one_or_none()
    if user is not None:
        flash(u'There is already an account associated with this email address.', 'danger')
        return register_page(formdata=request.form)
    user = db.User()
    user.screen_name = uuid.uuid4().hex
    user.name = request.form['name']
    user.email = request.form['email']
    user.password_hash = pbkdf2.gen(request.form['password'])
    user.sex = request.form['sex']
    user.birthday = request.form['dob'].replace('-', '')
    user.picture_id = 2
    db.session.add(user)
    db.session.commit()

    flash(u'Thanks for registering! Please login below.', 'success')
    return redirect(url_for('login_page'))


@app.route('/survey/1')
def survey1_page():
    return render_template('survey1.html')


@app.route('/survey/1', methods=['POST'])
def survey1():
    flash(u'Successfully submitted.', 'success')
    return redirect(url_for('surveys_page'))


@app.route('/survey/2')
def survey2_page():
    return render_template('survey2.html')


@app.route('/survey/2', methods=['POST'])
def survey2():
    flash(u'Successfully submitted.', 'success')
    return redirect(url_for('surveys_page'))


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/donate', methods=['GET'])
def donate_page():
    return render_template('donate.html')


@app.route('/donate', methods=['POST'])
def donate():
    flash(u'Thanks for donating!', 'success')
    return donate_page()


if __name__ == '__main__':
    app.run()

if not app.debug:
    import logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.WARNING)
    app.logger.addHandler(handler)
