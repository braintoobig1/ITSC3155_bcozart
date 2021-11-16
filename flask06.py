# FLASK Tutorial 1 -- We show the bare bones code to get an app up and running
from forms import RegisterForm
from flask import session
import bcrypt
from forms import LoginForm

#imports from flask4 assignment 
from models import Note as Note
from models import User as User


# imports
from database import db
from flask import request
from flask import redirect, url_for
import os                 # os is used to get environment variables IP & PORT
from flask import Flask  # Flask is the web app that we will customize
from flask import render_template


app = Flask(__name__)     # create an app
#This stuff under here is from the flassk 4 assignment

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db' #This will create a file called note_app_data.db file in the root directory of our application the first time the application is ran 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'SE3155'
#  Bind SQLAlchemy db object to this Flask app
db.init_app(app)
with app.app_context():
    db.create_all()   # run under the app context

#this is where it ends
# notes = {1: {'title': 'First note', 'text': 'This is my first note', 'date': '10-1-2020'},
#             2: {'title': 'Second note', 'text': 'This is my second note', 'date': '10-2-2020'},
#             3: {'title': 'Third note', 'text': 'This is my third note', 'date': '10-3-2020'}
#             }

# @app.route is a decorator. It gives the function "index" special powers.
# In this case it makes it so anyone going to "your-url/" makes this function
# get called. What it returns is what is shown as the web page
@app.route('/')
@app.route('/index')
def index():
    if session.get('user'):
        return render_template("index.html", user=session['user'])


    return render_template("index.html")

@app.route('/notes')
def get_notes():
    if session.get('user'):
        my_notes = db.session.query(Note).filter_by(user_id=session['user_id']).all()
        return render_template('notes.html', notes=my_notes, user=session['user'])
    else:
        return redirect(url_for('login'))
    #a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one() #Here we added a variable (a_user) to store our mock user data and we passed that variable to our template view (index.html) with a label called user.# 
    
    #my_notes = db.session.query(Note).all()
    #return render_template('notes.html', notes=my_notes , user = a_user)

@app.route('/notes/<note_id>')
def get_note(note_id):
    a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()
    #here
    my_note = db.session.query(Note).filter_by(id=note_id).one()
    return render_template('note.html', note=my_note, user = a_user)


@app.route('/notes/new', methods=['GET', 'POST'])
def new_note():
     #Here we added a variable (a_user) to store our mock user data and we passed that variable to our template view (index.html) with a label called user.#
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['noteText']
            from datetime import date
            today =date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Note(title, text, today)
            db.session.add(new_record)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
            a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()
            return render_template('new.html', user = session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/notes/edit/<note_id>', methods=['GET', 'POST'])
def update_note(note_id):
    if session.get('user'):

        if request.method == 'POST':
            title = request.form['title']
            text = request.form['noteText']
            note = db.session.query(Note).filter_by(id=note_id).one()

            note.title = title
            note.text = text

            db.session.add(note)
            db.session.commit()

            return redirect(url_for('get_notes'))
        else:
                a_user = db.session.query(User).filter_by(email='mogli@uncc.edu').one()
                my_note = db.session.query(Note).filter_by(id=note_id).one()
                return render_template('new.html', note=my_note, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/notes/delete/<note_id>', methods=['POST'])
def delete_note(note_id):
    if session.get('user'):

        my_note = db.session.query(Note).filter_by(id=note_id).one()
        db.session.delete(my_note)
        db.session.commit()

        return redirect(url_for('get_notes'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        # salt and hash password
        
        h_password = bcrypt.hashpw(
        request.form['password'].encode('utf-8'), bcrypt.gensalt())
        # get entered user data
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        # create user model
        new_user = User(first_name, last_name, request.form['email'], h_password)
        # add user to database and commit
        db.session.add(new_user)
        db.session.commit()
        # save the user's name to the session
        session['user'] = first_name
        session['user_id'] = new_user.id  # access id value from user model of this newly added user
        # show user dashboard view
        return redirect(url_for('get_notes'))

    # something went wrong - display register view
    return render_template('register.html', form=form)
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    # validate_on_submit only validates using POST
    if login_form.validate_on_submit():
        # we know user exists. We can use one()
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        # user exists check password entered matches stored password
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            # password match add user info to session
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            # render view
            return redirect(url_for('get_notes'))

        # password check failed
        # set error message to alert user
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        # form did not validate or GET request
        return render_template("login.html", form=login_form)

app.run(host=os.getenv('IP', '127.0.0.1'),port=int(os.getenv('PORT', 5000)),debug=True)

# To see the web page in your web browser, go to the url,
#   http://127.0.0.1:5000

# Note that we are running with "debug=True", so if you make changes and save it
# the server will automatically update. This is great for development but is a
# security risk for production. 