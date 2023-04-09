# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
import sql_func
import hashlib

flask_hook = 'flask webhook url'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
bootstrap = Bootstrap(app)
sql_func.create_db()
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=5, max=14)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=5, max=14)])
    remember = BooleanField('remember')

def log_check():
    if "logged" in session:
        try:
            x = session.get("logged")
            if sql_func.check_login(x[2],x[1]):
                return True
        except Exception as e:
            print(e)
    else:
        return False

@app.route('/')
def index():
    if log_check():
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/register')
def telegram_redirect():
    return redirect("https://t.me/AioFlaskBot")

@app.route('/sfalkjglkafgiuriterjvist83u2t0', methods=['GET', 'POST'])
def parse_request():
    try:
        data = request.json
        login = data["login"]
        password = data["password"].encode()
        hash_pwd = hashlib.sha256(password).hexdigest()
        user_id = data["user_id"]
        username = data["username"]
        user_tg = data["user_tg"]
        sql_func.insert_db(login,hash_pwd, user_id, username, user_tg)
    except Exception as e:
        print(e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = request.form.get('username')
        password = request.form.get('password').encode()
        remember = True if request.form.get('remember') else False
        hash_pwd = hashlib.sha256(password).hexdigest()
        try:
            if len(user) > 4 and len(user) < 15:
                if len(password) > 4 and len(password) < 15:
                    if sql_func.select_id('user_id',user, hash_pwd):
                        user_id = sql_func.select_id('user_id',user, hash_pwd)
                        if remember:
                            session.permanent = True
                            session['logged'] = (user_id,hash_pwd,user)
                            return redirect(url_for('dashboard'))
                        else:
                            session['logged'] = (user_id,hash_pwd,user)
                            return redirect(url_for('dashboard'))
            return '<h1>Не верный логин или пароль</h1>'
        except Exception as e:
            print(e)
            return '<h1>Не верный логин или пароль</h1>'
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if log_check():
        x = session.get("logged")
        print(x[2],x[1])
        telegram_name = sql_func.select_id('username',x[2], x[1])
        return render_template('dashboard.html',login = x[2],telegram_id = x[0][0][0],telegram_name = telegram_name[0][0])
    else:
        return redirect(url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(threaded=True)