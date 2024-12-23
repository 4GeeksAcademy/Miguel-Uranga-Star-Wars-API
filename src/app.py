"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os, json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Person, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#-------------------------------------USER---------------------------------#
#Getting the list of all users within the system.
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        all_users = User.query.all()
        if len(all_users) < 1:
            return jsonify({"msg": "There are no users registered in the platform."}), 400
        
        serialized_users = list(map(lambda x: x.serialize(), all_users))
        return serialized_users, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    
#Getting ta specific user within the system.
@app.route('/users/<int:user_id>', methods=['GET'])
def get_a_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": f"User {user_id} does not exist"}), 400
        
        serialized_user = user.serialize()
        return serialized_user, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    


@app.route('/users', methods=['POST'])
def create_a_user():
    try:
        request_body = json.loads(request.data)
        new_User = User(
            email = request_body["email"],
            password = request_body["password"],
            is_active = True
        )
        if not request_body:
            return jsonify({"msg": "No information was provided"}), 400
        
        db.session.add(new_User)
        db.session.commit()
        serialized_user = new_User.serialize()

        return jsonify({"msg": f"Created user: {serialized_user}"}), 200
    

    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    

#--------------------------PLANETS--------------------------------#

#Getting the list of all planets within the system.
@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        all_planets = Planet.query.all()
        if len(all_planets) < 1:
            return jsonify({"msg": "There are no planets registered in the platform."}), 400
        
        serialized_planets = list(map(lambda x: x.serialize(), all_planets))
        return serialized_planets, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    
#Getting the list of all planets within the system.
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_a_planet(planet_id):
    try:
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({"msg": f"The planet with id {planet_id} does not exist"}), 400
        
        serialized_planet = planet.serialize()
        return serialized_planet, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500


#--------------------------PERSON--------------------------------#

#Getting the list of all characters within the system.
@app.route('/people', methods=['GET'])
def get_all_characters():
    try:
        all_people = Person.query.all()
        if len(all_people) < 1:
            return jsonify({"msg": "There are no people registered in the platform."}), 400
        
        serialized_people = list(map(lambda x: x.serialize(), all_people))
        return serialized_people, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    
#Getting the list of all planets within the system.
@app.route('/people/<int:people_id>', methods=['GET'])
def get_a_character(people_id):
    try:
        person = Planet.query.get(people_id)
        if not person:
            return jsonify({"msg": f"The person with id {people_id} does not exist"}), 400
        
        serialized_people = person.serialize()
        return serialized_people, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    

#--------------------------FAVORITES--------------------------------#
#Getting all the favorites form a user
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_favorites_user(user_id):
    try:
        user_favorites = User.query.get(user_id)

        if not user_favorites:
            return jsonify({"msg": "This user is not registered in the platform."}), 400
        
        if len(user_favorites.favorites) < 1:
            return jsonify({"msg": "There are no favorites for this user."}), 400
        
        serialized_user_favorites = user_favorites.serialize_favorites()
        return serialized_user_favorites, 200
    

    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    

#Posting favorite planets to a specific user
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_new_favorite_planet(user_id, planet_id):
    try:
        user_favorites = User.query.get(user_id)

        if not user_favorites:
            return jsonify({"msg": "This user is not registered in the platform."}), 400
        


        #request_body = json.loads(request.data)
        new_favorite_Planet = Favorites(
            user_id = user_id,
            homeworld_id = planet_id
        )

        # if not request_body:
        #     return jsonify({"msg": "No information was provided"}), 400

        db.session.add(new_favorite_Planet)
        db.session.commit()
        serialized_favorites = user_favorites.serialize_favorites()

        return jsonify({"msg": f"Added a new favorite planet: {serialized_favorites}"}), 200
    
    
    
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500


#Posting favorite characters to a specific user
@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_new_favorite_character(user_id, people_id):
    try:
        user_favorites = User.query.get(user_id)

        if not user_favorites:
            return jsonify({"msg": "This user is not registered in the platform."}), 400
        


        #request_body = json.loads(request.data)
        new_favorite_Planet = Favorites(
            user_id = user_id,
            person_id = people_id
        )

        # if not request_body:
        #     return jsonify({"msg": "No information was provided"}), 400

        db.session.add(new_favorite_Planet)
        db.session.commit()
        serialized_favorites = user_favorites.serialize_favorites()

        return jsonify({"msg": f"Added a new favorite character! {serialized_favorites}"}), 200
    
    
    
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500

#-----------------------------------------DELETION-------------------------------------------------#
#Deleting favorite characters to a specific user
@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_a_favorite_character(user_id, people_id):
    try:
        deletable_favorites = Favorites.query.filter_by(user_id = user_id, person_id = people_id)
        deletable_favorites = list(map(lambda x: x, deletable_favorites))
        print(deletable_favorites)

        if not deletable_favorites:
            return jsonify({"msg": f"This character is not in user {user_id}'s favorites"}), 400
        
        for favorites in deletable_favorites:
            db.session.delete(favorites)
        db.session.commit()

        return jsonify({"msg": f"Removed user {user_id}'s registries of character {people_id}!"}), 200
    
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    

#Deleting favorite planets to a specific user
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_a_favorite_planet(user_id, planet_id):
    try:
        deletable_favorites = Favorites.query.filter_by(user_id = user_id, homeworld_id = planet_id)
        deletable_favorites = list(map(lambda x: x, deletable_favorites))
        #print(deletable_favorites)

        if not deletable_favorites:
            return jsonify({"msg": f"This character is not in user {user_id}'s favorites"}), 400
        
        for favorites in deletable_favorites:
            db.session.delete(favorites)
        db.session.commit()

        return jsonify({"msg": f"Removed user {user_id}'s registries of planet {planet_id}!"}), 200
    
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
