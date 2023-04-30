"""Server for movie ratings app."""
from flask import (Flask, render_template, request, flash, session, redirect)
import requests
from model import connect_to_db, db
import crud
import os

#from yelpapi import YelpAPI

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined

API_KEY = 'YELP_API_KEY'
#google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
#cuisine_types = ['Italian', 'Mexican', 'Chinese']

@app.route('/')
def homepage():
    """View homepage"""

    return render_template('homepage.html')


@app.route('/create_account', methods=['POST'])
def new_account():
    """Create a new account."""

    # if request.method =='POST':
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
    
    #return render_template('create_account.html')


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
            flash(f"Welcome, {user.email}!")
            # think about adding adding username, user_id to the session object here to access everywhere
            #when logging a user out, must also take out all, not just 1
            return redirect('/preferences')

    return render_template('login.html')


@app.route('/preferences', methods=['GET'])
def preferences():
    """Displays the page to enter user preferences in the form"""
    
    url = "https://api.yelp.com/v3/businesses/search?location=Los%20Angeles&term=restaurants&price=1&price=2&price=3&price=4&sort_by=best_match&limit=50"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + os.environ[API_KEY]
    }

    res = requests.get(url, headers=headers)
    json_data = res.json()
    print(json_data)
    cuisines = []

    for business in json_data['businesses']:
        for category in business['categories']:
            cuisines.append(category['title'])

    return render_template('preferences_form.html', cuisines=cuisines)

@app.route('/preferences', methods=['POST'])
def preferences_form():
    """Process the user's preferences from the form"""
    
    # Get user's preferences from form
    cuisine_type = request.form.get('cuisine_type')
    min_yelp_rating = request.form.get('min_yelp_rating')
    min_yelp_price = request.form.get('min_yelp_price')
    max_distance = request.form.get('max_distance')

    # need to create an instance when they submit the form, then add that instance to the db then commit
    preference = Preference(cuisine_type=cuisine_type,
                            min_yelp_rating=min_yelp_rating,
                            min_yelp_price=min_yelp_price,
                            max_distance=max_distance)
    
    db.session.add(preference)
    db.session.commit()

    flash ('Preferences submitted successfully!')
    #return redirect('/recommendations')

    return render_template('preferences_form.html', preference=preference)

@app.route('/recommendations')
def restaurant_recommendations():
    """Displays recommendations based on the user's preferences"""

    cuisine_type = request.args.get('title', '')
    min_yelp_rating = request.args.get('rating', '')
    min_yelp_price = request.args.get('price', '')
    max_distance = request.args.get('location', '')

    url = 'https://api.yelp.com/v3/businesses/search'
    payload = {'apikey': API_KEY,
               'title': cuisine_type,
               'rating': min_yelp_rating,
               'price': min_yelp_price,
               'location': max_distance}
    
    response = requests.get(url, params=payload)
    data = response.json()

    if '_embedded' in data:
        recommendations = data['_embedded']['recommendations']
    else:
        recommendations = []

    return render_template('recommendations.html',
                           pformat=pformat,
                           data=data,
                           results=recommendations)
    #if request.method == 'POST':
        # get user's preferences
        #preference = crud.get_preferences()

    #     url = "https://api.yelp.com/v3/businesses/search"
    #     # define parameters for Yelp Fusion API call
    #     headers = {
    #         'accept': 'application/json',
    #         'Authorization': 'API_KEY',
    #     }
    #     params = {
    #         'term': preference.cuisine_type,
    #         'price': preference.min_yelp_price + ',' + '4', # filter by min price and up to $$$$ (4 $ signs)
    #         'rating': preference.min_yelp_rating,
    #         'categories': 'restaurants', # only show results in the restaurants category
    # #     }

    #     # make GET request to Yelp Fusion API endpoint
    #     response = requests.get(url, headers=headers, params=params)

    #     # parse response data to extract relevant restaurant information
    #     data = json.loads(response.text)
    #     businesses = data.get('businesses', [])
    #     recommendations = []

    #     for business in businesses:
    #         name = business.get('name')
    #         rating = business.get('rating')
    #         price = business.get('price')
    #         categories = ', '.join([category.get('title') for category in business.get('categories', [])])
    #         address = ', '.join(business.get('location', {}).get('display_address', []))
    #         recommendation = {
    #             'name': name,
    #             'rating': rating,
    #             'price': price,
    #             'categories': categories,
    #             'address': address,
    #         }
    #         recommendations.append(recommendation)

    #     return render_template('recommendations.html', recommendations=recommendations)

    # return render_template('preferences_form.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)