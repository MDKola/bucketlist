from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import flash

from classes.users import Users
from classes.buckets import Buckets

app = Flask(__name__)
bucketlists = {}
users = Users()


@app.route('/')
def index():
    """Display the welcome page"""
    if users.user_is_logged_in is not None:
        return redirect('/dashboard')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Login the user"""
    if users.user_is_logged_in is not None:
        flash('You are not logged in to view this page.')
        return redirect('/dashboard')

    data = {}

    if request.method == 'GET':
        flash('Login to continue.')
        return render_template('login.html', data=data)

    if request.method == 'POST':

        email = request.form['email'].replace(" ", "")
        password = request.form['password']

        error = users.login(email, password)

        if error is not None:
            data['error'] = str(error)
            flash('Failed! Invalid inputs.')
            return render_template('login.html', data=data)
        else:
            flash("Welcome to the bucketlist. You are now logged in as {}".format(email))
            return redirect('/dashboard')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """Register a new user and login the user"""
    if users.user_is_logged_in is not None:
        return redirect('/dashboard')

    data = {}

    if request.method == 'GET':
        return render_template('register.html', data=data)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].replace(" ", "")
        password = request.form['password']
        confirm = request.form['confirm']

        error = users.register(name, email, password, confirm)

        if error is not None:
            data['error'] = str(error)
            flash('Failed! Invalid input')
            return render_template('register.html', data=data)
        else:
            users.login(email, password)
            flash('You are now looged in as {}'.format(email))
            return redirect('/dashboard')


@app.route('/logout', methods=['GET'])
def logout():
    """Logout the logged user"""
    users.logout()
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET'])
def display_bucket():
    """loop through the user's buckets and display the current buckets"""
    if users.user_is_logged_in is None:
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
    """Add a new bucketlist for the current logged in user"""
    bucket = request.form['bucket']
    if len(bucket.replace(" ", "")) == 0:
        flash('The bucket title cannot be empty!')
        return redirect('/dashboard')
    else:
        new_bucket = Buckets(bucket)
        current_user = users.user_is_logged_in

        if current_user in bucketlists.keys():
            bucketlists[current_user].append(new_bucket)
        else:
            bucketlists[current_user] = [new_bucket]
        flash('Bucketlist has been added successfully')
        return redirect('/dashboard')


@app.route('/edit/<bucket_id>', methods=['POST', 'GET'])
def edit_bucket(bucket_id):
    """Edit a bucket associated with the bucket_id"""
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
        flash('Bucket has been updated successfully')
        return redirect(url_for('display_bucket'))


@app.route('/dashboard/delete_bucket/<bucket_id>', methods=['GET', 'POST'])
def delete_bucket(bucket_id):
    """Delete a bucketlist from the user's bucketlists"""
    logged_in_user = users.user_is_logged_in

    if logged_in_user in bucketlists.keys():
        user_buckets = bucketlists[logged_in_user]

    count = 0
    for bucket in user_buckets:
        if str(bucket.id) == bucket_id:
            user_buckets.pop(count)
            break

        count += 1
    flash('Bucket deleted successfully')
    return redirect('/dashboard')


@app.route('/dashboard/<bucket_id>', methods=["GET"])
def view_bucket_activity(bucket_id):
    """Display the current activities under a selected bucket"""
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
    """Create a bucket activity under a selected bucketlist"""
    title = request.form['activity']
    if len(title.replace(" ", "")) == 0:
        flash("Activity title cannot be empty!")
        return redirect('/dashboard/' + bucket_id)
    else:
        logged_in_user = users.user_is_logged_in

        if logged_in_user in bucketlists.keys():
            user_buckets = bucketlists[logged_in_user]

        for bucket in user_buckets:
            if str(bucket.id) == bucket_id:
                bucket.create_activity(title)

        flash('Bucket item added successfully.')
        return redirect('/dashboard/' + bucket_id)


@app.route('/edit_activity/<activity_id>', methods=['POST', 'GET'])
def edit_activity(activity_id):
    """Edit an activity under a selected bucket"""
    if request.method == 'GET':
        return render_template('edit_activity.html', activity_id=activity_id)

    if request.method == 'POST':
        _id = request.form['id']
        new_title = request.form['new_title']

        logged_in_user = users.user_is_logged_in

        if logged_in_user in bucketlists.keys():
            user_bucket = bucketlists[logged_in_user]
        for bucket in user_bucket:
            bucket_id = str(bucket.id)

        for bucket in user_bucket:
            for item in bucket.bucket_activities:
                if str(item['id']) == activity_id:
                    bucket.update_activity(_id, new_title)
                    break
        flash('Item edited successfully')
        return redirect('/dashboard/' + bucket_id)


@app.route('/manage/<bucket_id>/delete/<activity_id>', methods=['GET', 'POST'])
def delete_activity(bucket_id, activity_id):
    """Delete a single bucketlist activity on the selected bucketlist"""
    logged_in_user = users.user_is_logged_in

    if logged_in_user in bucketlists.keys():
        user_buckets = bucketlists[logged_in_user]

    for bucket in user_buckets:
        if str(bucket.id) == bucket_id:
            for item in bucket.bucket_activities:
                if str(item['id']) == str(activity_id):
                    bucket.delete_activity(activity_id)
                    break
    flash('Item deleted successfully')
    return redirect('/dashboard/' + bucket_id)


app.secret_key = "secretkey"
if __name__ == '__main__':
    app.run(debug=True)
