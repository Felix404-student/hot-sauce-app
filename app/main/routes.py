from app.main import bp
from app.models.hotsauce import Rating, HotSauce
from app.models.user import User
from flask_bcrypt import Bcrypt
from app.extensions import db
from app.forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash, session

bcrypt = Bcrypt()


@bp.route('/')
def index():
    return render_template('index.html', title='Home')


@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('main.login'))
    return render_template('users/register.html', title='Register', form=form)


@bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@bp.route("/profile")
def profile():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if user_id:
        # Retrieve the user object from the database
        user = User.query.get(user_id)
        if user:
            # Retrieve the hot sauces rated by the user
            user_ratings = Rating.query.filter_by(user_id=user_id).all()
            rated_hotsauces = [HotSauce.query.get(rating.hotsauce_id) for rating in user_ratings]

            # Render the profile page with the user's information
            return render_template('users/profile.html', title='Profile', user=user, rated_hotsauces=rated_hotsauces)
        else:
            flash('User not found!', 'danger')
    else:
        flash('Please log in to view your profile.', 'danger')
        return redirect(url_for('main.login'))  # Redirect to the login page if the user is not logged in


@bp.route("/logout")
def logout():
    session.clear()  # Clear the session data
    flash('You have been logged out!', 'success')
    return redirect(url_for('main.index'))
