"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db, User, Preference, Restaurant, Visited, Favorite
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/create_account', methods=['GET', 'POST'])
def new_account():
    """Create a new account."""

    if request.method =='POST':
        # gets the form variables
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # if user already exists
        user = crud.get_user_by_email(email)

        if user:
            flash('That email is already in use, please try again.')
            return redirect('/create_account')

        # create and add new user to db
        user = crud.create_user(username, email, password)
        
        db.session.add(user)
        db.session.commit()

        flash('Account created successfully! Please log in.')
        return redirect('/login')
    
    return render_template('create_account.html')


@app.route('/login', methods=['GET', 'POST'])
def login_process():
    """Process the user login"""
    if request.method == 'POST':
        #QUESTION: should I remove the username?
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # if user exists
        user = crud.get_user_by_email(email)
   
        if not user or user.password != password:
            flash("The email or password you entered was incorrect.")
        else:
            session["user_email"] = user.email
            flash(f"Welcome, {user.email}!")

            return redirect('/preferences')

    return render_template('login.html')


@app.route('/preferences', methods=['GET'])
def preferences():
    """Displays the page to enter user preferences in the form"""

    return render_template('preferences_form.html')

@app.route('/preferences', methods=['POST'])
def preferences_form():
    """Process the user's preferences from the form"""
    # Get user's preferences from form
    # QUESTION: do these need "preference." before them to be an attribute of the instance of the Preference class?
    cuisine_type = request.form.get('cuisine_type')
    min_yelp_rating = request.form.get('min_yelp_rating')
    min_yelp_price = request.form.get('min_yelp_price')
    max_distance = request.form.get('max_distance')

    db.session.commit()

    flash ('Preferences submitted successfully!')
    return redirect('/recommendations')

@app.route('/recommendations')
def restaurant_recommendations():
    """Displays recommendations based on the user's preferences"""

    # get user's preferences
    preference = crud.get_preference_by_id(preference_id)

    # code here to call Yelp API

    # code here to call Google Maps API

    # code here to combine the 2?
    return render_template('recommendations.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)