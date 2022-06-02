from flask import render_template
from app import app
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for
from app.accounts_service import create_user, Checklogin_user
from flask_login import current_user,logout_user, login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Checklogin_user(form.username.data,form.password.data)
        if not user:
            flash("No hay una cuenta registrada con ese correo electronico", "error")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page', posts=posts)
    
if __name__ == '__main__':
    app.run(debug=True)
