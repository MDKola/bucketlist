from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from classes.users import Users
from classes.buckets import Buckets

app = Flask(__name__)
bucketlists = {}
users = Users()

@app.route('/')
def index():
	if users.user_is_logged_in is not None:
		return redirect('/dashboard')
	else:	
		return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if users.user_is_logged_in is not None:
		return redirect('/dashboard')

	data = {'host_url': request.host_url}

	if request.method == 'GET':
		return render_template('login.html', data=data)

	if request.method == 'POST':

		email = request.form['email']
		password = request.form['password']

		error = users.login(email, password)

		if error is not None:
			data['error'] = str(error)
			return render_template('login.html', data=data)
		else:
			return redirect('/dashboard')

	

@app.route('/register', methods=['POST', 'GET'])
def register():
	if users.user_is_logged_in is not None:
		return redirect('/dashboard')

	data = {'host_url': request.host_url}

	if request.method == 'GET':
		return render_template('register.html', data=data)

	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		confirm = request.form['confirm']

		error = users.register(name, email, password, confirm)

		if error is not None:
			data['error'] = str(error)
			return render_template('register.html', data=data)
		else:
			users.login(email, password)
			return redirect('/dashboard')

@app.route('/logout', methods=['GET'])
def logout():
	users.logout()
	return redirect(url_for('index'))

#display the buckets
@app.route('/dashboard', methods=['GET'])
def display_bucket():
	if users.user_is_logged_in == None:
		return redirect('/login')

	data = dict()
	data['host_url'] = request.host_url
	data['user_bucketlists'] = []
	logged_in_user = users.user_is_logged_in

	if logged_in_user in bucketlists.keys():
		user_bucketlists = bucketlists[logged_in_user]
		data['user_bucketlists'] = user_bucketlists
	return render_template('dashboard.html', data=data)
@app.route('/dashboard/add_bucket', methods=['POST'])
def add_bucket():
	bucket = request.form['bucket']
	new_bucket = Buckets(bucket)
	current_user = users.user_is_logged_in

	if current_user in bucketlists.keys():
		bucketlists[current_user].append(new_bucket)
	else:
		bucketlists[current_user] = [new_bucket]
	return redirect('/dashboard')

@app.route('/edit/<bucket_id>', methods=['POST', 'GET'])
def edit_bucket(bucket_id):
	if request.method == 'GET':
		return render_template('edit_bucket.html', bucket_id=bucket_id)

	if request.method == 'POST':
		id = request.form['id']
		new_title = request.form['new_title']

		
		logged_in_user = users.user_is_logged_in
		user_buckets = bucketlists[logged_in_user]

		for bucket in user_buckets:
			if str(bucket.id) == id:
				bucket.update_bucket(new_title)
				break
		return redirect(url_for('display_bucket'))
	


	


@app.route('/dashboard/delete_bucket/<bucket_id>', methods=['GET', 'POST'])
def delete_bucket(bucket_id):
	logged_in_user = users.user_is_logged_in

	if logged_in_user in bucketlists.keys():
		user_buckets = bucketlists[logged_in_user]

	count = 0
	for bucket in user_buckets:
		if str(bucket.id) == bucket_id:
			user_buckets.pop(count)
			break

		count += 1
	return redirect('/dashboard')
	

@app.route('/dashboard/<bucket_id>', methods=["GET"])
def view_bucket_activity(bucket_id):
	data = {'host_url': request.host_url}
	logged_in_user = users.user_is_logged_in
	data['current_bucket'] = bucket_id
	data['user_bucket'] = []

	if logged_in_user in bucketlists.keys():
		user_bucket = bucketlists[logged_in_user]
		data['user_bucket'] = user_bucket

	for bucket in user_bucket:
		if str(bucket.id) == bucket_id:
			data['user_activities'] = bucket.bucket_activities
			break
	return render_template('manage_bucket.html', data=data)

@app.route('/manage/<bucket_id>/add_activity', methods=['POST'])
def create_bucket_activity(bucket_id):
	title = request.form['activity']
	logged_in_user = users.user_is_logged_in

	if logged_in_user in bucketlists.keys():
		user_buckets = bucketlists[logged_in_user]

	for bucket in user_buckets:
		if str(bucket.id) == bucket_id:
			bucket.create_activity(title)
	return redirect('/dashboard/' + bucket_id)

@app.route('/edit_activity/<activity_id>', methods=['POST', 'GET'])
def edit_activity(activity_id):
	if request.method == 'GET':
		return render_template('edit_activity.html', activity_id=activity_id)

	if request.method == 'POST':
		print('I see you')
		id = request.form['id']
		new_title = request.form['new_title']
		print(new_title)
		print(id)

		
		logged_in_user = users.user_is_logged_in
		user_buckets = bucketlists[logged_in_user]
		print('user_bucket', user_buckets)

		for bucket in user_buckets:
			if str(bucket.id) == activity_id:
				if item in bucket.bucket_activities:
					if str(item['id']) == str(activity_id):
						bucket.update_activity(new_title)
						break
		
		return redirect('/dashboard')
		

@app.route('/manage/<bucket_id>/delete/<activity_id>', methods=['GET', 'POST'])
def delete_activity(bucket_id, activity_id):
	logged_in_user = users.user_is_logged_in

	if logged_in_user in bucketlists.keys():
		user_buckets = bucketlists[logged_in_user]

	for bucket in user_buckets:
		if str(bucket.id) == bucket_id:
			for item in bucket.bucket_activities:
				if str(item['id']) == str(activity_id):
					bucket.delete_activity(activity_id)
					break
	return redirect('/dashboard/' + bucket_id)


if __name__ == '__main__':
	app.run(debug=True)
