
from flask import render_template, url_for, flash, redirect, request
from edify import app, db, bcrypt
from edify.forms import RegistrationForm, LoginForm
from edify.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

import requests

posts =[{
	'author': 'Jitendar Singh',
	'title':'Whats up with me?',
	'content':'This is my first blog post, just checking out what all can be done',
	'date_posted':'July 1,2019'
},
{
	'author': 'Monalisa kaur',
	'title':'Full tension no attention!',
	'content':'This is my first blog post, just checking out what all can be done',
	'date_posted':'June 30,2019'
	
}
]



@app.route("/")
@app.route("/blog", methods=['GET', 'POST'])
@login_required
def blog():
	return render_template('blog.html', title='Blog',posts=posts)


@app.route("/feed")
def feed():

	url = ('https://newsapi.org/v2/everything?q=cricket&from=2019-06-02&sortBy=publishedAt&apiKey=22f1f27cdc17449baa2c855d949bd275')

	response = requests.get(url).json()
	article = response["articles"]
	
	return render_template('feed.html',article=article)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('blog'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in','success')
		return redirect(url_for('login'))
	return render_template('register.html',title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('blog'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('blog'))
		else:	
			flash('Login Unsuccessful. Please check email and password','danger')

	return render_template('login.html',title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('feed'))

@app.route("/account")
@login_required
def account():
	return render_template('account.html',title='Account')