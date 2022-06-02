from flask import render_template
from app import app
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, session, request
from app.accounts_service import create_user, login_User, get_profile
from app.models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = create_user(form.username.data, form.name.data, form.age.data, form.email.data, form.password.data)
        if not user:
            flash("A user with that email already exists.")
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = login_User(email, password)
        if not user:
            flash('Invalid login.')
        else:
            session['email'] = email
            flash('Logged in.')
            return redirect(url_for('index'))
    if request.method == 'GET':
        if "usr" in session:
            return redirect(url_for("index"))
        else:
            return render_template("login.html", title='Login', form=form)
    return render_template("login.html", title='Login', form=form)

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    if "email" in session:
        usr = session["email"]
        session["email"] = usr
        user_profile = get_profile(usr)
        return render_template("index.html", user_profile=user_profile)
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop("email", None)
    flash("You have successfully been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)
