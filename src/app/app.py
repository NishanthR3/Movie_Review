from flask import Flask, render_template, request, redirect, url_for, flash, session, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import user_database, theater_database, movie_database

# init Flask App
app = Flask(__name__)

# init database classes
user = user_database.User()
theatre = theater_database.Theater()
movie = movie_database.Movie()


@app.route('/')
def index():
    return render_template('home.html')

# --------------------- RegisterForm Class -------------------->
class RegisterForm(Form):
    name = StringField(
        'Name', [validators.DataRequired(), validators.Length(min=1, max=50)])
    username = StringField(
        'Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField(
        'Email', [validators.DataRequired(), validators.Length(min=6, max=50)])
    address = StringField(
        'Address', [validators.DataRequired(), validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password', [validators.DataRequired()])
# ------------------------------------------------------------->


#---------------- Logout Required Decorator ------------------>
def logged_out_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash("You need to logout first", 'danger')
            return redirect(url_for('index'))
        else:
            return f(*args, **kwargs)
    return wrap
# ------------------------------------------------------------>


# -------------------------- Register ------------------------->
@app.route('/register', methods=['GET', 'POST'])
@logged_out_required
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        # Back end handling here
        errorValue = user.register(request)
        if errorValue == 1:
            flash('User Name is already taken', 'danger')
        elif errorValue == 2:
            flash('Server could not respond', 'danger')
        else:
            flash('Successfully registered', 'success')
            return redirect(url_for('login'))        
        
    return render_template('register.html', form=form)
# ------------------------------------------------------------->


# -------------------------- Login --------------------------->
@app.route('/login', methods=['GET', 'POST'])
@logged_out_required
def login():

    if request.method == 'POST':

        # Back end handling here
        errorValue = user.authenticate(request)
        if errorValue == 0:
            flash('Logged in', 'success')
            return redirect(url_for('profile', username=request.form['username']))
        elif errorValue == 1:
            flash('Invalid credentials', 'danger')
        elif errorValue == 2:
            flash('Server error', 'danger')
    
    return render_template('login.html')
# ------------------------------------------------------------>


# -------------------------- Register ------------------------->
@app.route('/theatre_register', methods=['GET', 'POST'])
@logged_out_required
def theatre_register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        # Back end handling here
        errorValue = theatre.register(request)
        if errorValue == 1:
            flash('User Name is already taken', 'danger')
        elif errorValue == 2:
            flash('Server could not respond', 'danger')
        else:
            flash('Successfully registered', 'success')
            return redirect(url_for('theatre_login'))        
        
    return render_template('theatre_register.html', form=form)
# ------------------------------------------------------------->


# -------------------------- Login --------------------------->
@app.route('/theatre_login', methods=['GET', 'POST'])
@logged_out_required
def theatre_login():

    if request.method == 'POST':

        # Back end handling here
        errorValue = theatre.authenticate(request)
        if errorValue == 0:
            flash('Logged in', 'success')
            return redirect(url_for('index'))
        elif errorValue == 1:
            flash('Invalid credentials', 'danger')
        elif errorValue == 2:
            flash('Server error', 'danger')
    
    return render_template('theatre_login.html')
# ------------------------------------------------------------>


# ---------------- Login Required Decorator ------------------>
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", 'danger')
            return redirect(url_for('login'))
    return wrap
# ------------------------------------------------------------>


# ----------------------- User Profile ----------------------->
@app.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def profile(username):

    # Stop user from accessing other users' profiles
    if username != session['username']:
        flash("You need to login as " + username + " to access their private profile.", 'danger')
        return redirect(url_for('profile', username=session['username']))

    # Get trending movies to display
    temp = movie.movies_list()
    movies_list = []
    for item in temp[1]:
        movies_list.append({
            'name': item[0],
            'percent': round((100/3 * int(item[1]) / int(item[2])), 2)
        })
    
    movies_list.sort(key=lambda x: x['percent'])
    movies_list.reverse()

    return render_template('profile.html', movies_list=movies_list)
# ------------------------------------------------------------>


# -------------------- Add Show for theatre ------------------>
@app.route('/add_show', methods=['GET', 'POST'])
@login_required
def add_show():

    if 'theatre' not in session:
        flash("You do not have theatre admin access", 'danger')
        return redirect(url_for('/'))
    
    if request.method == 'POST':
        # back end handling here
        return redirect(url_for('add_show'))
    
    temp = movie.movies_list()

    movies_list = []
    for movies in temp[1]:
        movies_list.append({
            'movie_id': movies[3],
            'name': movies[0]
        })
    
    return render_template('add_show.html', movies_list=movies_list)
# ------------------------------------------------------------>


# ----------------- Delete Show for theatre ------------------>
@app.route('/delete_show', methods=['GET', 'POST'])
@login_required
def delete_show():

    if 'theatre' not in session:
        flash("You do not have theatre admin access", 'danger')
        return redirect(url_for('/'))
    
    return render_template('delete_show.html')
# ------------------------------------------------------------>


# -------------------------- Logout -------------------------->
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    flash("You have been logged out", 'success')
    return redirect(url_for('index'))
# ------------------------------------------------------------>


if __name__ == '__main__':
    app.secret_key = '1\xceg\xe1\xde\x96A$d6\x8e\xf0*\x07\xe6\xbezM\x9f}\xc2\x97P\xba'
    app.run(debug=True, threaded=True)
