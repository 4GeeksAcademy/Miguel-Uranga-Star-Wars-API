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


#Getting the list of all users within the system.
@app.route('/user', methods=['GET'])
def get_all_users():
    try:
        all_users = User.query.all()
        if len(all_users) < 1:
            return jsonify({"msg": "There are no users registered in the platform."}), 400
        
        serialized_users = list(map(lambda x: x.serialize(), all_users))
        return serialized_users, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    
#Getting the list of all users within the system.
@app.route('/user/<int:user_id>', methods=['GET'])
def get_a_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"msg": f"User {user_id} does not exist"}), 400
        
        serialized_user = user.serialize()
        return serialized_user, 200
    except Exception as error:
        return jsonify({"msg": "Server error", "error":str(error)}), 500
    


@app.route('/user', methods=['POST'])
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


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
