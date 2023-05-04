"""Server for movie ratings app."""
from flask import (Flask, render_template, request, flash, session, redirect)
import requests
from model import connect_to_db, db, User, Preference
import crud
import os

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['YELP_API_KEY']
#google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

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
        else:
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
        email = request.form.get("email")
        password = request.form.get("password")

        # if user exists
        user = crud.get_user_by_email(email)
   
        if not user or user.password != password:
            flash("The email or password you entered was incorrect.")
        else:
            session["user_email"] = user.email
            session["user_id"] = user.user_id
            session["username"] = user.username
            flash(f"Welcome, {user.username}!")
            # think about adding adding username, user_id to the session object here to access everywhere
            #when logging a user out, must also take out all, not just 1
            return redirect('/preferences')

    return render_template('login.html')


@app.route('/preferences', methods=['GET'])
def preferences():
    """Displays the page to enter user preferences in the form"""
    
    #url = "https://api.yelp.com/v3/businesses/search"
    url = "https://api.yelp.com/v3/businesses/search?location=Los%20Angeles&term=restaurants&price=1&price=2&price=3&price=4&sort_by=best_match&limit=50"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    #reformat this payload so that it forms the url query string
    # payload = {'title': 'cuisine_type',
    #            'rating': 'min_yelp_rating',
    #            'price': 'min_yelp_price',
    #            'zip_code': 'zipcode'}
    # params = {}

    # if request.method == 'GET':
    #     params['title'] = request.args.get('title')
    #     params['rating'] = request.args.get('rating')
    #     params['price'] = request.args.get('price')
    #     params['zip_code'] = request.args.get('zip_code')


    res = requests.get(url, headers=headers)

    json_data = res.json()
    print(json_data)
    cuisines = []
    cuisines_set = set()

    for business in json_data['businesses']:
        for category in business['categories']:
            cuisine = category.get('title')
            if cuisine and cuisine not in cuisines_set:
                cuisines.append(cuisine)
                cuisines_set.add(cuisine)

    ratings = []
    for business in json_data['businesses']:
        rating = business['rating']
        if rating not in ratings:
            ratings.append(rating)

    prices = []
    for business in json_data['businesses']:
        price = business['price']
        if price not in prices:
            prices.append(price)

    return render_template('preferences_form.html', cuisines=cuisines, ratings=ratings, prices=prices)



@app.route('/preferences', methods=['POST'])
def preferences_form():
    """Process the user's preferences from the form"""
    #retrieve user object from session
    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)
    #session["user_id"] = user.user_id

    # Get user's preferences from form
    cuisine_type = request.form.get('cuisine_type')
    min_yelp_rating = request.form.get('min_yelp_rating')
    min_yelp_price = request.form.get('min_yelp_price')
    max_distance = request.form.get('max_distance')
    zipcode = request.form.get('zipcode')

    # need to create an instance when they submit the form, then add that instance to the db then commit
    preference = user.preferences

    preference = Preference(user_id=user.user_id,
                            cuisine_type=cuisine_type,
                            min_yelp_rating=min_yelp_rating,
                            min_yelp_price=min_yelp_price,
                            max_distance=max_distance,
                            zipcode=zipcode
                            )
    

    db.session.add(preference)
    
    # preference.cuisine_type = cuisine_type
    # preference.min_yelp_rating = min_yelp_rating
    # preference.min_yelp_price = min_yelp_price
    # preference.max_distance = max_distance
    # preference.zipcode = zipcode

    db.session.commit()

    flash ('Preferences submitted successfully!')
    return redirect('/recommendations')

    #return render_template('preferences_form.html', preference=preference)

@app.route('/recommendations')
def restaurant_recommendations():
    """Displays recommendations based on the user's preferences"""

    # get user's prefs from form data
    cuisine_type = request.form.get('title')
    min_yelp_rating = request.form.get('rating')
    min_yelp_price = request.form.get('price')
    #max_distance = request.form('max_distance')
    zipcode = request.form.get('zip_code')

    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {'title': cuisine_type,
               'rating': min_yelp_rating,
               'price': min_yelp_price,
               'zip_code': int(zipcode)}
    #check if it expects an int value and not a string for zip code
    
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)