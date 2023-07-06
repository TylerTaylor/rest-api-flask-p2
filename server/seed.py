# Imports
    # app from app
    # db and Models from models

from app import app
from models import db, Service, Show

# Create application context
    # with app.app_context():
    # Info on application context: https://flask.palletsprojects.com/en/1.1.x/appcontext/
with app.app_context():
    
# Create a query to delete all existing records
    print("Deleting existing services...")
    Service.query.delete()
    print("Deleting existing shows...")
    Show.query.delete()

# Create some seed data and commit to the database
    print("Creating new services...")
    s1 = Service(name='netflix', price=19.99)
    s2 = Service(name='hulu', price=14.99)
    s3 = Service(name='amazon prime', price=9.99)

    services = [s1, s2, s3]

    # stage our session with updated data
    db.session.add_all(services)
    # commit the changes to our database
    db.session.commit()
    print("Services added!")

    # Day 2
    print("Creating new shows...")
    show1 = Show(name='Squid Games', seasons=1, service_id=1)
    show2 = Show(name='Dave', seasons=3, service_id=2)
    show3 = Show(name='The Boys', seasons=4, service_id=3)

    shows = [show1, show2, show3]

    db.session.add_all(shows)
    db.session.commit()
    print("Shows added!")

# Run in terminal
    # python seed.py

# Test queries in Flask Shell