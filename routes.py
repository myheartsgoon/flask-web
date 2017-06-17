# coding=utf-8
from flask import Flask, render_template, request, redirect, session, url_for, flash
from models import db, User
from forms import SignupForm, LoginForm, AddressForm



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@127.0.0.1/flask_web'
db.init_app(app)

app.secret_key = 'development-key'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('home'))

    form = SignupForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("signup.html", form=form)
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash("Email has been used, please use another one!")
            return render_template("signup.html", form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            session['email'] = newuser.email
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template("signup.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return  redirect(url_for('home'))

    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = email
                return redirect(url_for('home'))
            else:
                flash('Email address or password incorrect!')
                return render_template('login.html', form=form)
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/home', methods=['POST', 'GET'])
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    form = AddressForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('home.html', form=form)
        else:
            pass
    elif request.method == 'GET':
        return render_template('home.html', form=form)

@app.route('/map')
def map():
    return render_template('map.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run('127.0.0.1', port=5000, debug=True)
