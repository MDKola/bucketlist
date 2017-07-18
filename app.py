from flask import Flask, redirect, render_template, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

from classes.users import Users

users = Users()
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
	data = {'host_url': request.host_url}
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		error = users.register(name, email, password)

		if error is not None:
			data['error'] = str(error)
			return render_template('register.html', data=data)
		else:
			users.login(email, password)
			return redirect('home.html')
	
	

	


if __name__ == '__main__':
	app.run(debug=True)
