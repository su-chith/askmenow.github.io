from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Question, Category, Answer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('Username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/search' , methods=['POST'])
@login_required
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        results = User.query.filter(User.username.ilike(f'%{search_query}%')).all()
        return render_template('search.html', results=results, user=current_user)
    return render_template('search.html', user=current_user)


@auth.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    if user is None:
        flash('User not found.')
        return None
    if user == current_user:
        flash('You cannot unfollow yourself.')
        return None
    current_user.unfollow(user)
    db.session.commit()
    flash('You have unfollowed {}.'.format(user.username))
    return redirect(url_for('auth.show_following', username=current_user.username))

@auth.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user is None:
        flash('User not found.')
        return None
    if user == current_user:
        flash('You cannot follow yourself.')
        return None
    current_user.follow(user)
    db.session.commit()
    flash('You have followed {}.'.format(user.username))
    return redirect(url_for('auth.show_following', username=user.username))



@auth.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    answers = Answer.query.filter_by(user_id=user.id).all()
    len_answers = len(answers)
    questions = Question.query.filter_by(user_id=user.id).all()
    len_questions = len(questions)
    len_followers = user.followers.count()
    len_following = user.following.count()
    return render_template('profile-answers.html', user=user, len_answers=len_answers, len_questions=len_questions, len_followers=len_followers, len_following=len_following)


@auth.route('/profile/<username>/questions/<category>')
@login_required
def show_questions_category(username, category):
    user = User.query.filter_by(username=username).first_or_404()
    answers = Answer.query.filter_by(user_id=user.id).all()
    len_answers = len(answers)
    questions = Question.query.filter_by(user_id=user.id).all()
    len_questions = len(questions)
    len_followers = user.followers.count()
    len_following = user.following.count()
    category = Category.query.filter_by(name=category).first()
    category_id = category.id
    questions_category = Question.query.filter_by(user_id=user.id, category_id=category_id).all()
    return render_template('pro-que-category.html', user=user, category=category, questions=questions_category, len_questions=len_questions, len_followers=len_followers, len_following=len_following, len_answers=len_answers)


@auth.route('/profile/<username>/questions')
@login_required
def show_questions(username):
    user = User.query.filter_by(username=username).first_or_404()
    answers = Answer.query.filter_by(user_id=user.id).all()
    len_answers = len(answers)
    questions = Question.query.filter_by(user_id=user.id).all()
    len_questions = len(questions)
    len_followers = user.followers.count()
    len_following = user.following.count()
    return render_template('questions.html', user=user, len_questions=len_questions, len_followers=len_followers, len_following=len_following, questions=questions, len_answers=len_answers)


@auth.route('/profile/<username>/followers')
@login_required
def show_followers(username):
    user = User.query.filter_by(username=username).first_or_404()
    answers = Answer.query.filter_by(user_id=user.id).all()
    len_answers = len(answers)
    questions = Question.query.filter_by(user_id=user.id).all()
    len_questions = len(questions)
    len_followers = user.followers.count()
    len_following = user.following.count()
    followers = user.followers.all()
    return render_template('followers.html', user=user, followers=followers, len_questions=len_questions, len_followers=len_followers, len_following=len_following, len_answers=len_answers)

@auth.route('/profile/<username>/following')
@login_required
def show_following(username):
    user = User.query.filter_by(username=username).first_or_404()
    answers = Answer.query.filter_by(user_id=user.id).all()
    len_answers = len(answers)
    questions = Question.query.filter_by(user_id=user.id).all()
    len_questions = len(questions)
    len_followers = user.followers.count()
    len_following = user.following.count()
    following = user.following.all()
    return render_template('following.html', user=user, following=following, len_questions=len_questions, len_followers=len_followers, len_following=len_following, len_answers=len_answers)

