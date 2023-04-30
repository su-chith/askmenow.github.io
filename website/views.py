from flask import Blueprint,render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json
from .models import Question, Category, Answer
from PIL import Image
from werkzeug.utils import secure_filename
import os

views = Blueprint('views', __name__)

# with open('path/to/image.png', 'rb') as f:
#     img_data = f.read()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    answers = Answer.query.all()
    return render_template('home.html', user=current_user, answers=answers)


@views.route('/answer', methods=['GET', 'POST'])
@login_required
def answer():
    questions = Question.query.all()
    
    return render_template('answer.html', user=current_user, questions=questions)


@views.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    categories = Category.query.all()
    questions = Question.query.all()
    return render_template('category.html', user=current_user, questions=questions)

@views.route('/category/<category>', methods=['GET', 'POST'])
@login_required
def category_answers(category):
    category = Category.query.filter_by(name=category).first()
    category_id = category.id
    questions = Question.query.filter_by(category_id=category_id).all()
    return render_template('category.html', user=current_user, questions=questions)


@views.route('/profile/<username>/questions/<int:question_id>', methods=['DELETE'])
@login_required
def delete_question(username, question_id):
    question = Question.query.filter_by(id=question_id, user=current_user).first()
    if question:
        db.session.delete(question)
        db.session.commit()
        flash('Your question has been deleted!', 'success')
    return jsonify({'success': True})




@views.route('/create-question', methods=['GET', 'POST'])
@login_required
def create_question():
    if request.method == 'POST':
        question = request.form.get('question')
        category = request.form.get('category')

        if len(question) < 1:
            flash('Question is too short.', category='error')
        else:
            category = Category.query.filter_by(name=category).first()
            if category:
                category_id = category.id
                new_question = Question(question=question, category_id=category_id, user_id=current_user.id)
                db.session.add(new_question)
                db.session.commit()
                flash('Question created!', category='success')
                return redirect(url_for('auth.show_questions', username=current_user.username))
            else:
                flash('Category does not exist.', category='error')
        return redirect(url_for('auth.show_questions'))




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@views.route('/<category>/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(category,question_id):
    question = Question.query.filter_by(id=question_id).first()
    category = Category.query.filter_by(name=category).first()
    from main import app
    if request.method == 'POST':

        answer = request.form.get('answer')
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        question_id = question_id
        question = Question.query.filter_by(id=question_id).first()
        new_answer = Answer(answer=answer, question_id=question_id, user_id=current_user.id, photo=filename)
        db.session.add(new_answer)
        db.session.commit()
        flash('Answer created!', category='success')
        return render_template('question.html', user=current_user, question=question, category=category)

    return render_template('question.html', user=current_user, question=question, category=category)


@views.route('/following', methods=['GET', 'POST'])
@login_required
def following():
    following = current_user.following

    return render_template('following_page.html', user=current_user, following=following)
