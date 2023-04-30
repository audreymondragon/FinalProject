"""CRUD operations"""
from model import db, User, Preference, Restaurant, Visited, Favorite, connect_to_db

def create_user(username, email, password):
    """Create and return a new user"""

    user = User(username=username, email=email, password=password)
    # db.session.add(user)
    # db.session.commit()

    return user

def get_users():
    """Return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()


def create_preference(user, cuisine_type, min_yelp_rating, min_yelp_price, max_distance):
    """Create and return a user's preferences"""

    preference = Preference(user=user, cuisine_type=cuisine_type, min_yelp_rating=min_yelp_rating, min_yelp_price=min_yelp_price, max_distance=max_distance)

    return preference

def get_preferences():
    """Return all preferences"""

    return Preference.query.all()

def get_preference_by_id(preference_id):
    """Return a preference by primary key."""

    return Preference.query.get(preference_id)



def create_restaurant(restaurant_name, yelp_rating, yelp_price, location):
    """Create and return a user's restaurants"""

    restaurant = Restaurant(restaurant_name=restaurant_name, yelp_rating=yelp_rating, yelp_price=yelp_price, location=location)

    return restaurant

def get_restaurants():
    """Return all restaurants"""

    return Restaurant.query.all()

def get_restaurant_by_id():
    """Return a restaurant by primary key"""

    return Restaurant.query.get(restaurant_id)



def create_visited(user, restaurant, visited, wishlist, location, yelp_api_restaurant_id):
    """Create and return a user's visited restaurants"""

    visited = Visited(user=user, restaurant=restaurant, visited=visited, wishlist=wishlist, location=location, yelp_api_restaurant_id=yelp_api_restaurant_id)

    return visited

def get_visited():
    """Return all visited restaurants"""

    return Visited.query.all()

def get_visited_by_id():
    """Return a visited restaurant by primary key"""

    return Visited.query.get(user_restaurant_id)



def create_favorite(user, restaurant):
    """Create and return a user's favorite restaurants"""

    favorite = Favorite(user=user, restaurant=restaurant)

    return favorite

def get_favorite():
    """Return all favorite restaurants"""

    return Favorite.query.all()

def get_favorite_by_id():
    """Return a favorite restaurant by primary key"""

    return Favorite.query.get(fav_restaurant_id)


    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)