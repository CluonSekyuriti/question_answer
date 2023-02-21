from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from werkzeug.utils import secure_filename
import os
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'static/product_img'
app.config['SECRET_KEY'] = "ajbfsgnhnegrb"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    admin = Column(Boolean)
    teacher = Column(Boolean)
    student = Column(Boolean)


class Question(db.Model):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question_text = Column(String)
    answer_text = Column(String)
    teacher_id = Column(Integer)
    student_id = Column(Integer, ForeignKey('user.id'))


with app.app_context():
    db.create_all()


def get_current_user():
    user_result = None
    if "username" in session:
        user_result = User.query.filter(User.username == session['username']).first()
    return user_result


@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('login'))


@app.route('/register_user', methods=['POST', 'GET'])
def register_user():
    user = get_current_user()
    if request.method == "POST":
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        hashed_password = generate_password_hash(user_password, method="sha256")
        add = User(username=user_name, password=hashed_password, student=True)
        db.session.add(add)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('index5.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user_name = request.form.get('user_name')
        user_password = request.form.get('user_password')
        get_user = User.query.filter(User.username == user_name).first()
        if get_user:
            checked = check_password_hash(get_user.password, user_password)
            session['username'] = user_name
            if checked:
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    return render_template('index5.html')


@app.route('/', methods=['POST', 'GET'])
def home():
    user = get_current_user()
    return render_template('index1.html', user=user)


@app.route('/add_teacher/<int:user_id>')
def add_teacher(user_id):
    user_info = User.query.filter(User.id == user_id).first()
    if user_info.teacher == True:
        User.query.filter(User.id == user_id).update({
            "teacher": False,
            "student": False
        })
    else:
        User.query.filter(User.id == user_id).update({
            "teacher": True,
            "student": False
        })
    db.session.commit()
    return redirect(url_for('settings', user_info=user_info))


@app.route('/add_student/<int:user_id>')
def add_student(user_id):
    user_info = User.query.filter(User.id == user_id).first()
    if user_info.student == True:
        User.query.filter(User.id == user_id).update({
            "student": False,
            "teacher": False
        })
    else:
        User.query.filter(User.id == user_id).update({
            "student": True,
            "teacher": False
        })
    db.session.commit()
    return redirect(url_for('settings', user_info=user_info))


@app.route('/questionlist')
def questionlist():
    user = get_current_user()
    return render_template('index11.html', user=user)


@app.route('/question', methods=['POST', 'GET'])
def question():
    user = get_current_user()
    teachers = User.query.filter(User.teacher == True).order_by(User.id).all()
    return render_template('index2.html', user=user, teachers=teachers)


@app.route('/settings')
def settings():
    user = get_current_user()
    users = User.query.order_by(User.id).all()
    return render_template('index3.html', users=users, user=user)


@app.route('/change')
def change():
    user = get_current_user()
    return render_template('index4.html', user=user)


@app.route('/change2')
def change2():
    user = get_current_user()
    return render_template('index44.html', user=user)


if __name__ == '__main__':
    app.run()
