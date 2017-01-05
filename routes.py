from flask import Flask, render_template, redirect, session, flash, url_for, Markup, request, g
from functools import wraps
import sqlite3
import os

#The path to the database depends on wether you run locally or remote.

folder = '' if os.path.isdir(r'c:\Anaconda3') else '/home/AndreRoukema/mysite/'
DATABASE = '{folder}sales.db'.format(folder=folder)

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'AGD67fGHJdjkd6768&**&dfdhd'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('log'))
    return wrap


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('log'))


@app.route('/test')
def test():
    test = ''
    flash('flash_message_test')
    for i in range(100):
        Markup('Number : {i}<br/>'.format(i=i))
    return render_template('test.html', test=test)


@app.route('/log', methods=['GET', 'POST'])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('hello'))
    return render_template('log.html', error=error)


@app.route('/hello')
@login_required
def hello():
    g.db = connect_db()
    cur = g.db.execute('select rep_name, amount from reps')
    sales = [dict(rep_name=row[0], amount=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('hello.html', sales=sales)


if __name__ == '__main__':
    app.run(debug=False)

