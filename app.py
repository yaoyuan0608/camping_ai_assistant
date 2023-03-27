from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired, InputRequired
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    meetings = db.relationship('Meeting', backref='user', lazy=True)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    room = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

class MeetingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    room = SelectField('Room', choices=[('Room A', 'Room A'), ('Room B', 'Room B'), ('Room C', 'Room C')], validators=[DataRequired()])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
    return render_template('start.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/schedule', methods=['POST','GET'])
@login_required
def schedule():
    form = MeetingForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        date = form.date.data
        start_time = datetime.combine(date, form.start_time.data)
        end_time = datetime.combine(date, form.end_time.data)
        room = form.room.data
        meeting = Meeting(title=title, description=description, date=date, start_time=start_time, end_time=end_time, room=room, user_id=current_user.id)
        db.session.add(meeting)
        db.session.commit()
        flash('Meeting has been scheduled successfully!', 'success')
        time.sleep(2)
        return redirect(url_for('dashboard'))
    return render_template('schedule.html', form=form)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # create a default user for testing purposes
        admin = User(username='admin', password='123',)
        db.session.add(admin)
        db.session.commit()

    app.run(debug=True)
