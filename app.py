from flask import Flask, redirect, render_template, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

from classes.buckets import Buckets
bucketlists = {}

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

@app.route('/add_bucket', methods=['POST'])
def add_bucket():
	bucketlist = request.form['bucketlist']
	new_bucketlist = Buckets(bucketlist)
	bucketlists.append(new_bucketlist)
	return redirect('/dashboard')


		
if __name__ == '__main__':
	app.run(debug=True)