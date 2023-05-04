"""Models for restaurant selector app"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    preferences = db.relationship("Preference", back_populates="user")
    favorites = db.relationship("Restaurant", secondary="fav_restaurants", back_populates="users")
    restaurant_visited = db.relationship("Visited", back_populates="user")
    # each visit will only have 1 user

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'

class Preference(db.Model):
    """A user's preferences"""

    __tablename__ = 'preferences'

    preference_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    cuisine_type = db.Column(db.String)
    min_yelp_rating = db.Column(db.Float)
    min_yelp_price = db.Column(db.String)
    max_distance = db.Column(db.Integer)
    zipcode = db.Column(db.Integer)

    user = db.relationship("User", back_populates="preferences")

    def __repr__(self):
        return f'<Preference preference_id={self.preference_id} cuisine_type={self.cuisine_type}>'

class Restaurant(db.Model):
    """A restaurant"""

    __tablename__ = 'restaurants'

    restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_name = db.Column(db.String)
    yelp_rating = db.Column(db.Integer)
    yelp_price = db.Column(db.Integer)
    location = db.Column(db.String)

    visited_by = db.relationship("Visited", back_populates="restaurant")
    users = db.relationship("User", secondary="fav_restaurants", back_populates="favorites")
    # 1 visit will be 1 restaurant
    # 1 user will have many fav restaurants

    def __repr__(self):
        return f'<Restaurant restaurant_id={self.preference_id} restaurant_name={self.restaurant_name}>'

class Visited(db.Model):
    """Restaurants a user has visited."""

    __tablename__ = 'restaurants_visited'

    user_restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))
    visited = db.Column(db.Boolean)
    wishlist = db.Column(db.Boolean)
    location = db.Column(db.String)
    yelp_api_restaurant_id = db.Column(db.Integer)

    user = db.relationship("User", back_populates="restaurant_visited")
    restaurant = db.relationship("Restaurant", back_populates="visited_by")
   
    def __repr__(self):
        return f'<Visited user_restaurant_id={self.user_restaurant_id} location={self.location}>'

class Favorite(db.Model):
    """A user's favorite restaurants"""

    __tablename__ = 'fav_restaurants'

    fav_restaurant_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.restaurant_id"))
   
    def __repr__(self):
        return f'<Favorite fav_restaurant_id={self.fav_restaurant_id} ____={self.____}>'



def connect_to_db(flask_app, db_uri="postgresql:///restaurants", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)