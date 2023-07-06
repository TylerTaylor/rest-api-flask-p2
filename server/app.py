#!/usr/bin/env python3

# Review:
    # REST
    # Status Codes
    # Error Handling

# Set Up:
    # Run in terminal:
        # cd server
        # export FLASK_APP=app.py
        # export FLASK_RUN_PORT=5555
        # flask db init
        # flask db revision --autogenerate -m "Create table <table name>"
        # flask db upgrade
        # python seed.py

    # Double check the database to verify the migration worked as expected
    

# RESTful routing examples

# |  HTTP Verb  |      Path       |      Description      |
# |-------------|-----------------|-----------------------|
# | GET         |  /services      | READ all resources    |
# | GET         |  /services/:id  | READ one resource     |
# | POST        |  /services      | CREATE one resource   |
# | PATCH/PUT   |  /services/:id  | UPDATE one resource   |
# | DELETE      |  /services/:id  | DESTROY one resource  |
# |-------------|-----------------|-----------------------|

# Status code reference: https://httpstatusdogs.com/

from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate

from flask_restful import Api, Resource

# 1. Import NotFound from werkzeug.exceptions for error handling

from models import db, Service, Show

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False # configures JSON responses to print on indented lines

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# 2. Use the `@app.errorhandler()` decorator to handle Not Found
    # 2.1 Create the decorator and pass in NotFound as a parameter
    # 2.2 Use make_response to create a response with a message and status of 404 (not found)
    # 2.3 Return the response

class Services(Resource):
    def get(self):
        service_list = [service.to_dict() for service in Service.query.all()]

        response = make_response(service_list, 200)
        return response

    def post(self):
        # Grab the form data from our request object and create a new Service
        request_json = request.get_json()
        new_service = Service(name=request_json['name'], price=request_json['price'])

        # Save to database and commit
        db.session.add(new_service)
        db.session.commit()

        # Return our new object as JSON response
        response_dict = new_service.to_dict()
        response = make_response(response_dict, 201)

api.add_resource(Services, '/services')

class Shows(Resource):
    def get(self):
        show_list = [show.to_dict() for show in Show.query.all()]

        response = make_response(show_list, 200)
        return response

    def post(self):
        # Grab the form data from our request object and create a new Show
        request_json = request.get_json()
        new_show = Show(
            name=request_json['name'],
            seasons=request_json['seasons'],
            service_id=request_json['service_id']
        )

        # Save to database and commit
        db.session.add(new_show)
        db.session.commit()

        # Return our new object as JSON response
        response_dict = new_show.to_dict()
        response = make_response(response_dict, 201)

api.add_resource(Shows, '/shows')

class ServiceById(Resource):
    def get(self, id):
        service = Service.query.filter(Service.id == id).first().to_dict()

# 3a. If the service is not found, raise an exception

        response = make_response(service, 200)
        return response

api.add_resource(ServiceById, '/services/<int:id>')

class ShowById(Resource):
    def get(self, id):
        show = Show.query.filter(Show.id == id).first()

# 3b. If the show is not found, raise an exception

        response = make_response(show.to_dict(), 200)
        return response

api.add_resource(ShowById, '/shows/<int:id>')

# 4. Patch
    # 4.1 Create a patch method that takes self and id as parameters
    # 4.2 Query the Service via the id
    # 4.3 If the Service is not found, raise an exception
    # 4.4 Loop through the request.get_json object and update the provided attributes. Note: Be cautious of data types
    # 4.5 Add and commit to the database
    # 4.6 Create + return a response

# 5. Delete
    # 5.1 Create a delete method, pass in self and an id
    # 5.2 Query the service via the id
    # 5.3 If the service is not found, raise an exception
    # 5.4 Delete the service and commit
    # 5.5 Create a ressponse with status 204 and return the response