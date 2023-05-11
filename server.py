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
API_KEY_GOOGLE = os.environ['GOOGLE_MAPS_API_KEY']
cuisines = ["Afghan",  "African",  "American (New)",  "American (Traditional)",  "Andalusian",  "Arabian",  "Argentine",  "Armenian",  "Asian Fusion",  "Asturian",  "Australian",  "Austrian",  "Baguettes",  "Bangladeshi",  "Barbeque",  "Basque",  "Bavarian",  "Beer Garden",  "Beer Hall",  "Beisl",  "Belgian",  "Bistros",  "Black Sea",  "Brasseries",  "Brazilian",  "Breakfast & Brunch",  "British",  "Buffets",  "Bulgarian",  "Burgers",  "Burmese",  "Cafes",  "Cafeteria",  "Cajun/Creole",  "Cambodian",  "Canadian (New)",  "Canteen",  "Caribbean",  "Dominican",  "Haitian",  "Puerto Rican",  "Trinidadian",  "Catalan",  "Cheesesteaks",  "Chicken Shop",  "Chicken Wings",  "Chilean",  "Chinese",  "Comfort Food",  "Corsican",  "Creperies",  "Cuban",  "Curry Sausage",  "Cypriot",  "Czech",  "Czech/Slovakian",  "Danish",  "Delis",  "Diners",  "Dinner Theater",  "Dumplings",  "Eastern European",  "Eritrean",  "Ethiopian",  "Fast Food",  "Filipino",  "Fischbroetchen",  "Fish & Chips",  "Flatbread",  "Fondue",  "Food Court",  "Food Stands",  "Freiduria",  "French",  "Galician",  "Game Meat",  "Gastropubs",  "Georgian",  "German",  "Giblets",  "Gluten-Free",  "Greek",  "Guamanian",  "Halal",  "Hawaiian",  "Heuriger",  "Himalayan/Nepalese",  "Honduran",  "Hong Kong Style Cafe",  "Hot Dogs",  "Hot Pot",  "Hungarian",  "Iberian",  "Indian",  "Indonesian",  "International",  "Irish",  "Island Pub",  "Israeli",  "Italian",  "Japanese",  "Donburi",  "Gyudon",  "Oyakodon",  "Hand Rolls",  "Horumon",  "Izakaya",  "Japanese Curry",  "Kaiseki",  "Kushikatsu",  "Oden",  "Okinawan",  "Okonomiyaki",  "Onigiri",  "Ramen",  "Robatayaki",  "Soba",  "Sukiyaki",  "Takoyaki",  "Tempura",  "Teppanyaki",  "Tonkatsu",  "Udon",  "Unagi",  "Western Style Japanese Food",  "Yakiniku",  "Yakitori",  "Jewish",  "Kebab",  "Kopitiam",  "Korean",  "Kosher",  "Kurdish",  "Laos",  "Laotian",  "Latin American",  "Colombian",  "Salvadoran",  "Venezuelan",  "Live/Raw Food",  "Lyonnais",  "Malaysian",  "Mamak",  "Nyonya",  "Meatballs",  "Mediterranean",  "Falafel",  "Mexican",  "Eastern Mexican",  "Jaliscan",  "Northern Mexican",  "Oaxacan",  "Pueblan",  "Tacos",  "Tamales",  "Yucatan",  "Middle Eastern",  "Egyptian",  "Lebanese",  "Milk Bars",  "Modern Australian",  "Modern European",  "Mongolian",  "Moroccan",  "New Mexican Cuisine",  "New Zealand",  "Nicaraguan",  "Night Food",  "Nikkei",  "Noodles",  "Norcinerie",  "Open Sandwiches",  "Oriental",  "Pakistani",  "Pan Asian",  "Parent Cafes",  "Parma",  "Persian/Iranian",  "Peruvian",  "PF/Comercial",  "Pita",  "Pizza",  "Polish",  "Pierogis",  "Polynesian",  "Pop-Up Restaurants",  "Portuguese",  "Potatoes",  "Poutineries",  "Pub Food",  "Rice",  "Romanian",  "Rotisserie Chicken",  "Russian",  "Salad",  "Sandwiches",  "Scandinavian",  "Schnitzel",  "Scottish",  "Seafood",  "Serbo Croatian",  "Signature Cuisine",  "Singaporean",  "Slovakian",  "Somali",  "Soul Food",  "Soup",  "Southern",  "Spanish",  "Sri Lankan",  "Steakhouses",  "Supper Clubs",  "Sushi Bars",  "Swabian",  "Swedish",  "Swiss Food",  "Syrian",  "Tabernas",  "Taiwanese",  "Tapas Bars",  "Tapas/Small Plates",  "Tavola Calda",  "Tex-Mex",  "Thai",  "Traditional Norwegian",  "Traditional Swedish",  "Trattorie",  "Turkish",  "Ukrainian",  "Uzbek",  "Vegan",  "Vegetarian",  "Venison",  "Vietnamese",  "Waffles",  "Wok",  "Wraps",  "Yugoslav"]

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
    #why is login not redirecting em to preferences?
    return render_template('login.html')


@app.route('/preferences', methods=['GET'])
def preferences():
    """Displays the page to enter user preferences in the form"""

    return render_template('preferences_form.html', cuisines=cuisines)


@app.route('/preferences', methods=['POST'])
def preferences_form():
    """Process the user's preferences from the form"""
    #retrieve user object from session
    user_id = session['user_id']
    user = crud.get_user_by_id(user_id)
    print(user_id)
    print(user)

    url = "https://api.yelp.com/v3/businesses/search?"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    #format this payload so that it forms the url query string
    payload = {'location': request.form.get('search_location'),
               'categories': 'Restaurants',
               'radius': request.form.get('radius'),
               'term': request.form.get('cuisine_type'),
               'price': request.form.get('min_yelp_price'),
               'sort_by': request.form.get('sort_by'),
               'limit': request.form.get('num_results')}
    print(payload)
    res = requests.get(url, headers=headers, params=payload)
    json_data = res.json()
    print(json_data)

    # Get user's preferences from form
    cuisine_type = request.form.get('cuisine_type')
    search_location = request.form.get('search_location')
    search_term = 'Restaurants'
    radius = request.form.get('radius')
    min_yelp_price = request.form.get('min_yelp_price')
    sort_by = request.form.get('sort_by')
    num_results = request.form.get('num_results')
    mode_transportation = request.form.get('mode_transportation')
    # need to add mode so we can use for google maps

    # need to create an instance when they submit the form, then add that instance to the db then commit
    #preference = user.preferences

    #preference = Preference(user_id=user.user_id,
                            # cuisine_type=cuisine_type,
                            # search_location=search_location,
                            # search_term=search_term,
                            # radius=radius,
                            # min_yelp_price=min_yelp_price,
                            # sort_by=sort_by,
                            # num_results=num_results,
                            # mode_transportation=mode_transportation
                            # )
    #print(preference)
    print('!!!!!!!!!!!!!!!!!!!!!')

    # db.session.add(preference)

    # db.session.commit()

    flash ('Preferences submitted successfully!')
    # return redirect('/recommendations')

    url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    payload = {'origins': request.form.get('search_location'),
               'destinations': '1015 3rd Street, Santa Monica CA, 90403',
                'mode': request.form.get('mode_transportation'),
                'units': 'imperial',
                'key': f'{API_KEY_GOOGLE}'
                }
    headers = {}

    #need to figure out how to get the display address from restaurants in the destinations

    print(payload)
    print('^^^^^^^^^^^^^^^^^^^^^^^')
    response = requests.get(url, headers=headers, params=payload)
    #maps_json = response.json()
    print(response)
    print(response.text)
    print('+++++++++++++++++++++++')

    return (json_data)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)