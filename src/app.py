"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User

from models import db, User, People, Planet, Vehicle, FavoritePeople, FavoritePlanets, FavoriteVehicles
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


######################################
# Configure logging

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
######################################

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


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response"
    }

    return jsonify(response_body), 200


#########################################################################################
#########################################################################################
#############                        Star Wars Blog                         #############
#############                           REST API                            #############
#############                          Endpoints                            #############
#########################################################################################
#########################################################################################
"""
Extra changes from original requirements:

    - Added an endpoint to [GET] the information of just one user (only name and username)

    - Changed URL endpoint for getting all the favorites from a single user

    - Added "user_id" to POST/DELETE request endpoints for favorite planet and people

    - Grouping:
        - Group all the CRUD operations for PEOPLE and PLANETS
        - Group User's endpoints
        - Group Favorite handling


    |-----------------------------------------------------------------------------------
    |-----------------  edited ....... INSTRUCTIIONS AND REQUIREMENTS  -----------------
    |-----------------------------------------------------------------------------------
    |
    |
    |       -- CRUD operations: PEOPLE and PLANETS --
    |
    |-----------
    |    People's information [GET], [POST], [PUT] and [DELETE]:
    |        [] Get list of ALL PEOPLE ----------------> [GET]    /people
    |        [] Get ONE PERSON ------------------------> [GET]    /people/<int:people_id>
    |        [] Add one PEOPLE ------------------------> [POST]   /people
    |        [] Update one PEOPLE ---------------------> [PUT]    /people/<int:people_id>
    |        [] Delete one PEOPLE ---------------------> [DELETE] /people/<int:people_id>
    |
    |-----------
    |    Planets' information [GET], [POST], [PUT] and [DELETE]:
    |        [] Get list of ALL PLANETS ---------------> [GET]    /planets
    |        [] Get ONE PLANET ------------------------> [GET]    /planets/<int:planet_id>
    |        [] Add one PLANET ------------------------> [POST]   /planets
    |        [] Update one PLANET ---------------------> [PUT]    /planets/<int:planet_id>
    |        [] Delete one PLANET ---------------------> [DELETE] /planets/<int:planet_id>
    |
    |
    |-----------------------------------------------------------------------
    |
    |
    |       -- USERS --
    |
    |-----------
    |    [GET] User's information:
    |        [] Get list of ALL USERS -----------------> [GET]  /users
    |        [] Get One User info ---------------------> [GET]  /user/<int:user_id>  ..................................... (EXTRA endpoint)
    |
    |
    |-----------------------------------------------------------------------
    |
    |
    |       -- FAVORITE's Handling --
    |
    |-----------
    |    Favorites from One USER:
    |        [] One user, ALL Favorites ---------------> [GET]    /user/<int:user_id>/favorites  ......................... CHANGED URL ENDPOINT
    |
    |-----------
    |    Adding new favorites:
    |        [] Add One PLANET ------------------------> [POST]   /user/<int:user_id>/favorite/planet/<int:planet_id> .... INCLUDED USER ID
    |        [] Add One PEOPLE ------------------------> [POST]   /user/<int:user_id>/favorite/people/<int:people_id> .... INCLUDED USER ID
    |
    |-----------
    |    Deleting favorites:
    |        [] Delete One PLANET ---------------------> [DELETE] /user/<int:user_id>/favorite/planet/<int:planet_id> .... INCLUDED USER ID
    |        [] Delete One PEOPLE ---------------------> [DELETE] /user/<int:user_id>/favorite/people/<int:people_id> .... INCLUDED USER ID
    |
    |
    |---------------------------------------------------------------------------------------------------
"""




###############################################################################################################################################################################




#########################################################################################
#########################################################################################
#############                        PEOPLE ENDPOINTS                       #############
#########################################################################################
#########################################################################################



############################################
#######    Get list of ALL PEOPLE    #######
############################################
@app.route('/people', methods=['GET'])
def get_all_people():

    try:
        people = People.query.all()
        return jsonify({
            'total': len(people),
            'data': [person.serialize() for person in people]
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_all_people: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_all_people: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######     Get ONE PERSON by ID     #######
############################################
@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_person(people_id):
    
    try:
        person = People.query.get(people_id)

        if not person:
            return jsonify({
                'success': False,
                'message': f'Person with ID {people_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': person.serialize()
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_one_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_one_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######         Add one PERSON       #######
############################################
""" JSON example
{
    "name": "Darth Vader",
    "birth_year": "41.9BBY",
    "eye_color": "yellow",
    "gender": "male", 
    "hair_color": "none",
    "height": "202",
    "mass": "136",
    "skin_color": "white",
    "homeworld": "Tatooine",
    "url": "https://swapi.dev/api/people/4/"
}
"""
@app.route('/people', methods=['POST'])
def add_person():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        # Validate required fields
        required_fields = ['name', 'birth_year', 'eye_color', 'gender', 'hair_color', 'height', 'mass', 'skin_color', 'homeworld', 'url']

        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Create new person
        new_person = People(
            name       = data['name'],
            birth_year = data['birth_year'],
            eye_color  = data['eye_color'],
            gender     = data['gender'],
            hair_color = data['hair_color'],
            height     = data['height'],
            mass       = data['mass'],
            skin_color = data['skin_color'],
            homeworld  = data['homeworld'],
            url        = data['url']
        )

        db.session.add(new_person)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Person created successfully',
            'data': new_person.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in add_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Data integrity error - possibly duplicate URL',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in add_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in add_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######       Update one PERSON      #######
############################################
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):

    try:
        person = People.query.get(people_id)

        if not person:
            return jsonify({
                'success': False,
                'message': f'Person with ID {people_id} not found'
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        # Update fields if provided
        updatable_fields = ['name', 'birth_year', 'eye_color', 'gender', 'hair_color','height', 'mass', 'skin_color', 'homeworld', 'url']
        
        for field in updatable_fields:
            if field in data:
                setattr(person, field, data[field])

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Person updated successfully',
            'data': person.serialize()
        }), 200

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in update_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Data integrity error - possibly duplicate URL',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in update_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in update_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######       Delete one PERSON      #######
############################################
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):

    try:
        person = People.query.get(people_id)

        if not person:
            return jsonify({
                'success': False,
                'message': f'Person with ID {people_id} not found'
            }), 404

        db.session.delete(person)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Person with ID {people_id} deleted successfully'
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in delete_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in delete_person: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500



#########################################################################################
#########################################################################################
#############                        PLANET ENDPOINTS                       #############
#########################################################################################
#########################################################################################


############################################
#######    Get list of ALL PLANETS   #######
############################################
@app.route('/planets', methods=['GET'])
def get_all_planets():

    try:
        planets = Planet.query.all()

        return jsonify({
            'success': True,
            'total': len(planets),
            'data': [planet.serialize() for planet in planets]
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_all_planets: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_all_planets: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######     Get ONE PLANET by ID     #######
############################################
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
   
    try:
        planet = Planet.query.get(planet_id)

        if not planet:
            return jsonify({
                'success': False,
                'message': f'Planet with ID {planet_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': planet.serialize()
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_one_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_one_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######     Add one PLANET     #######
############################################
""" JSON example
{
    "name": "Tatooine",
    "diameter": "10465",
    "rotation_period": "23",
    "orbital_period": "304",
    "gravity": "1 standard",
    "population": "200000",
    "climate": "arid",
    "terrain": "desert",
    "surface_water": "1",
    "url": "https://swapi.dev/api/planets/1/"
}
"""
@app.route('/planets', methods=['POST'])
def add_planet():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        # Validate required fields
        required_fields = ['name', 'diameter', 'rotation_period', 'orbital_period', 'gravity', 'population', 'climate', 'terrain', 'surface_water', 'url']

        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Create new planet
        new_planet = Planet(
            name            = data['name'],
            diameter        = data['diameter'],
            rotation_period = data['rotation_period'],
            orbital_period  = data['orbital_period'],
            gravity         = data['gravity'],
            population      = data['population'],
            climate         = data['climate'],
            terrain         = data['terrain'],
            surface_water   = data['surface_water'],
            url             = data['url']
        )

        db.session.add(new_planet)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Planet created successfully',
            'data': new_planet.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in add_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Data integrity error - possibly duplicate URL',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in add_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in add_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######       Update one PLANET      #######
############################################
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):

    try:
        planet = Planet.query.get(planet_id)

        if not planet:
            return jsonify({
                'success': False,
                'message': f'Planet with ID {planet_id} not found'
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        # Update fields if provided
        updatable_fields = ['name', 'diameter', 'rotation_period', 'orbital_period', 'gravity', 'population', 'climate', 'terrain', 'surface_water', 'url']
        
        for field in updatable_fields:
            if field in data:
                setattr(planet, field, data[field])

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Planet updated successfully',
            'data': planet.serialize()
        }), 200

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in update_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Data integrity error - possibly duplicate URL',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in update_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in update_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######       Delete one PLANET      #######
############################################
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    try:
        planet = Planet.query.get(planet_id)

        if not planet:
            return jsonify({
                'success': False,
                'message': f'Planet with ID {planet_id} not found'
            }), 404

        db.session.delete(planet)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Planet with ID {planet_id} deleted successfully'
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in delete_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in delete_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500




#########################################################################################
#########################################################################################
#############                      VEHICLE ENDPOINTS                        #############
#########################################################################################
#########################################################################################


############################################
#######   Get list of ALL VEHICLES   #######
############################################
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():

    try:
        vehicles = Vehicle.query.all()

        return jsonify({
            'success': True,
            'data': [vehicle.serialize() for vehicle in vehicles],
            'total': len(vehicles)
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_all_vehicles: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_all_vehicles: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######     Get ONE VEHICLE by ID    #######
############################################
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):

    try:
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return jsonify({
                'success': False,
                'message': f'Vehicle with ID {vehicle_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': vehicle.serialize()
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_one_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_one_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######        Add one VEHICLE       #######
############################################
""" JSON example
{
    "name": "Sand Crawler",
    "model": "Digger Crawler",
    "vehicle_class": "wheeled",
    "manufacturer": "Corellia Mining Corporation",
    "length": "36.8",
    "cost_in_credits": "150000",
    "crew": "46",
    "passengers": "30",
    "max_atmos_speed": "30",
    "cargo_capacity": "50000",
    "consumables": "2 months",
    "url": "https://swapi.dev/api/vehicles/4/"
}
"""
@app.route('/vehicles', methods=['POST'])
def add_vehicle():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        # Validate required fields
        required_fields = ['name', 'model', 'vehicle_class', 'manufacturer', 'length', 'cost_in_credits', 'crew', 'passengers', 'max_atmos_speed', 'cargo_capacity', 'consumables', 'url']
        
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Create new vehicle
        new_vehicle = Vehicle(
            name            = data['name'],
            model           = data['model'],
            vehicle_class   = data['vehicle_class'],
            manufacturer    = data['manufacturer'],
            length          = data['length'],
            cost_in_credits = data['cost_in_credits'],
            crew            = data['crew'],
            passengers      = data['passengers'],
            max_atmos_speed = data['max_atmos_speed'],
            cargo_capacity  = data['cargo_capacity'],
            consumables     = data['consumables'],
            url             = data['url']
        ) 

        db.session.add(new_vehicle)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Vehicle created successfully',
            'data': new_vehicle.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in add_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Data integrity error - possibly duplicate URL',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in add_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in add_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######      Update one VEHICLE      #######
############################################
@app.route('/vehicles/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):

    try:
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return jsonify({
                'success': False,
                'message': f'Vehicle with ID {vehicle_id} not found'
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        # Update fields if provided
        updatable_fields = ['name', 'model', 'vehicle_class', 'manufacturer', 'length', 'cost_in_credits', 'crew', 'passengers', 'max_atmos_speed', 'cargo_capacity', 'consumables', 'url']
        
        for field in updatable_fields:
            if field in data:
                setattr(vehicle, field, data[field])

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Vehicle updated successfully',
            'data': vehicle.serialize()
        }), 200

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in update_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Data integrity error - possibly duplicate URL',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in update_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in update_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######      Delete one VEHICLE      #######
############################################
@app.route('/vehicles/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):

    try:
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return jsonify({
                'success': False,
                'message': f'Vehicle with ID {vehicle_id} not found'
            }), 404

        db.session.delete(vehicle)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Vehicle with ID {vehicle_id} deleted successfully'
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in delete_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in delete_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500




#########################################################################################
#########################################################################################
#############                         USER ENDPOINTS                        #############
#########################################################################################
#########################################################################################

""" JSON example
{
    "email": "luke@jedi.com",
    "username": "luke_skywalker",
    "name": "Luke Skywalker",
    "password": "force123",
    "is_active": true
}
"""

############################################
#######    Get list of ALL USERS     #######
############################################
@app.route('/users', methods=['GET'])
def get_all_users():

    try:
        users = User.query.all()

        return jsonify({
            'success': True,
            'data': [user.serialize() for user in users],
            'total': len(users)
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_all_users: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_all_users: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
#######       Get One User info      #######
############################################
@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': user.serialize()
        }), 200
    
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_one_user: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_one_user: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500




#########################################################################################
#########################################################################################
#############                      FAVORITES ENDPOINTS                      #############
#########################################################################################
#########################################################################################



############################################
#######   One user, ALL Favorites    #######
############################################
@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404

        return jsonify({
            'success': True,
            'user_id': user_id,
            'favorites': {
                'people':   [fav.serialize() for fav in user.favorite_people],
                'planets':  [fav.serialize() for fav in user.favorite_planets],
                'vehicles': [fav.serialize() for fav in user.favorite_vehicles]
            },
            'totals': {
                'people':   len(user.favorite_people),
                'planets':  len(user.favorite_planets),
                'vehicles': len(user.favorite_vehicles)
            }
        }), 200

    except SQLAlchemyError as e:
        logger.error(f"Database error in get_user_favorites: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in get_user_favorites: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500




##########################################################
################    ADDING FAVORITES    ##################
##########################################################


############################################
#######  Add One PLANET to favorites #######
############################################
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):

    try:
        # Check if user exists
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404

        # Check if planet exists
        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({
                'success': False,
                'message': f'Planet with ID {planet_id} not found'
            }), 404

        # Check if already favorited
        existing_favorite = FavoritePlanets.query.filter_by(
            user_id=user_id, 
            planet_id=planet_id
        ).first()
        
        if existing_favorite:
            return jsonify({
                'success': False,
                'message': f'Planet {planet.name} is already in user\'s favorites'
            }), 409

        # Create new favorite
        new_favorite = FavoritePlanets(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Planet {planet.name} added to favorites successfully',
            'data': new_favorite.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in add_favorite_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'This planet is already in your favorites',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in add_favorite_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in add_favorite_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
####### Add One PEOPLE to favorites  #######
############################################
@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):

    try:
        # Check if user exists
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404

        # Check if person exists
        person = People.query.get(people_id)

        if not person:
            return jsonify({
                'success': False,
                'message': f'Person with ID {people_id} not found'
            }), 404

        # Check if already favorited
        existing_favorite = FavoritePeople.query.filter_by(
            user_id=user_id, 
            people_id=people_id
        ).first()
        
        if existing_favorite:
            return jsonify({
                'success': False,
                'message': f'{person.name} is already in user\'s favorites'
            }), 409

        # Create new favorite
        new_favorite = FavoritePeople(user_id=user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'{person.name} added to favorites successfully',
            'data': new_favorite.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in add_favorite_people: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'This person is already in your favorites',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in add_favorite_people: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in add_favorite_people: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
####### Add One VEHICLE to favorites #######
############################################
@app.route('/user/<int:user_id>/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):

    try:
        # Check if user exists
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404

        # Check if vehicle exists
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return jsonify({
                'success': False,
                'message': f'Vehicle with ID {vehicle_id} not found'
            }), 404

        # Check if already favorited
        existing_favorite = FavoriteVehicles.query.filter_by(
            user_id=user_id, 
            vehicle_id=vehicle_id
        ).first()
        
        if existing_favorite:
            return jsonify({
                'success': False,
                'message': f'{vehicle.name} is already in user\'s favorites'
            }), 409

        # Create new favorite
        new_favorite = FavoriteVehicles(user_id=user_id, vehicle_id=vehicle_id)
        db.session.add(new_favorite)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'{vehicle.name} added to favorites successfully',
            'data': new_favorite.serialize()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error in add_favorite_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'This vehicle is already in your favorites',
            'error': str(e)
        }), 409
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in add_favorite_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in add_favorite_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500




##########################################################
###############    DELETING FAVORITES    #################
##########################################################


############################################
##### Delete One PLANET from favorites #####
############################################
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):

    try:
        # Check if user exists
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404

        # Find the favorite relationship
        favorite = FavoritePlanets.query.filter_by(
            user_id=user_id, 
            planet_id=planet_id
        ).first()
        
        if not favorite:
            return jsonify({
                'success': False,
                'message': f'Planet with ID {planet_id} is not in user\'s favorites'
            }), 404

        planet_name = favorite.planet.name

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'{planet_name} removed from favorites successfully'
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in delete_favorite_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in delete_favorite_planet: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
##### Delete One PEOPLE from favorites #####
############################################
@app.route('/user/<int:user_id>/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):

    try:
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404

        # Find the favorite relationship
        favorite = FavoritePeople.query.filter_by(
            user_id=user_id, 
            people_id=people_id
        ).first()
        
        if not favorite:
            return jsonify({
                'success': False,
                'message': f'Person with ID {people_id} is not in user\'s favorites'
            }), 404

        person_name = favorite.people.name
        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'{person_name} removed from favorites successfully'
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in delete_favorite_people: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in delete_favorite_people: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500


############################################
##### Delete One VEHICLE from favorites ####
############################################
@app.route('/user/<int:user_id>/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):

    try:
        # Check if user exists
        user = User.query.get(user_id)

        if not user:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404

        # Find the favorite relationship
        favorite = FavoriteVehicles.query.filter_by(
            user_id=user_id, 
            vehicle_id=vehicle_id
        ).first()
        
        if not favorite:
            return jsonify({
                'success': False,
                'message': f'Vehicle with ID {vehicle_id} is not in user\'s favorites'
            }), 404

        vehicle_name = favorite.vehicle.name

        db.session.delete(favorite)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'{vehicle_name} removed from favorites successfully'
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error in delete_favorite_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Database error occurred',
            'error': str(e)
        }), 500
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in delete_favorite_vehicle: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(e)
        }), 500





##################################################################################################################################
##################################################################################################################################

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)



