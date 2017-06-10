from flask import Flask, render_template, request, redirect
from models import db, User
from forms import SignupForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1/flask_web'
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
    form = SignupForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("signup.html", form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            return "Successful"
    elif request.method == 'GET':
        return render_template("signup.html", form=form)

if __name__ == "__main__":
    app.run('127.0.0.1', port=5000, debug=True)