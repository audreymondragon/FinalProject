"""CRUD operations"""
from model import db, User, Preference, Restaurant, Visited, Favorite, connect_to_db

def create_user(username, email, password):
    """Create and return a new user"""

    user = User(username=username, email=email, password=password)

    return user


def create_preference(cuisine_type, min_yelp_rating, min_yelp_price, max_distance):
    """Create and return a user's preferences"""

    preference = Preference(cuisine_type=cuisine_type, min_yelp_rating=min_yelp_rating, min_yelp_price=min_yelp_price, max_distance=max_distance)

    return preference


def create_restaurant(restaurant_name, yelp_rating, yelp_price, location):
    """Create and return a user's restaurants"""

    restaurant = Restaurant(restaurant_name=restaurant_name, yelp_rating=yelp_rating, yelp_price=yelp_price, location=location)

    return restaurant

def create_visited(visited, wishlist, location, yelp_api_restaurant_id):
    """Create and return a user's visited restaurants"""

    visited = Visited(visited=visited, wishlist=wishlist, location=location, yelp_api_restaurant_id=yelp_api_restaurant_id)

    return visited
    
if __name__ == '__main__':
    from server import app
    connect_to_db(app)