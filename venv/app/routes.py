from flask import render_template
from app import app
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = create_user(form.username.data, form.email.data, form.password.data)
        if not user:
            flash("A user with that email already exists.")
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form, username=username, password=password)

if __name__ == '__main__':
    app.run(debug=True)
