from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
#Creacion de la tabla de planetas
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    diameter = db.Column(db.String(10), unique=False, nullable=False)
    rotation_period = db.Column(db.String(10), unique=False, nullable=False)
    orbital_period = db.Column(db.String(10), unique=False, nullable=False)
    population = db.Column(db.String(10), unique=False, nullable=False)
    terrain = db.Column(db.String(10), unique=False, nullable=False)
    surface_water = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }


#Creacion de la tabla de personajes
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    birth_year = db.Column(db.String(15), unique=False, nullable=False)
    eye_color = db.Column(db.String(15), unique=False, nullable=False)
    gender = db.Column(db.String(10), unique=False, nullable=False)
    hair_color = db.Column(db.String(15), unique=False, nullable=False)
    height = db.Column(db.String(3), unique=False, nullable=False)
    height = db.Column(db.String(3), unique=False, nullable=False)
    """ homeworld_id = db.Column(db.Integer, db.ForeignKey(Planet.id), nullable=False)
    homeworld = db.relationship(Planet)
    """
    def __repr__(self):
        return '<Person %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "Planet":self.homeworld,
            "planet_id": self.homeworld_id
        }


#Creacion de la tabla de favoritos
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)
    person_id = db.Column(db.Integer, db.ForeignKey(Person.id), nullable=True)
    person = db.relationship(Person)
    homeworld_id = db.Column(db.Integer, db.ForeignKey(Planet.id), nullable=True)
    homeworld = db.relationship(Planet)

    def __repr__(self):
        return '<Favorites %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "Person": self.person,
            "Homeworld": self.homeworld,
        }
