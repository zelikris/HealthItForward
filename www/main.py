from binascii import unhexlify
from urllib.parse import urljoin

import db
import pbkdf2
import sessions
from flask import Flask, render_template, request, session, g, redirect, url_for

app = Flask(__name__)
app.secret_key = unhexlify('e3d7f0871b236241be434fe4cc789f2e72b970b5a13502488a2d259574911b65')
app.session_interface = sessions.JWTSessionInterface()


@app.before_request
def before_request():
    g.user = None
    if 'sub' in session:
        g.user = db.session.query(db.User).filter_by(email=session['sub']).one_or_none()


@app.teardown_appcontext
def teardown_db_session(exception=None):
    db.session.remove()


@app.route('/profile')
@sessions.login_required
def profile():
    return 'hi'  # TODO


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
        # TODO: show an error
        return login_page()


@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    # TODO: persist
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)
