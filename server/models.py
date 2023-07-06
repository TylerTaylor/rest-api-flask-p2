from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_serializer import SerializerMixin

# 6. Import validates from sqlalchemy.orm
from sqlalchemy.orm import validates

# Initialize our db
db = SQLAlchemy()

class Service(db.Model, SerializerMixin):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    shows = db.relationship('Show', backref='service')

    serialize_rules = ('-shows.service',) # This is a tuple, so if there's only one item, you need the trailing comma or it will yell

# 7. Use the "validates" decorator to create a validation for name OR price
    @validates('price')
    def validates_price(self, key, price_input):
        # import ipdb; ipdb.set_trace()
        if not isinstance(price_input, float):
            raise ValueError("Price must be in XX.XX format")
        return round(price_input, 2)

        # if isinstance(price_input, float):
        #     return price_input
        # # raise error

    def __repr__(self):
        return f"<Service Name: {self.name}, Price: ${self.price}>"

class Show(db.Model, SerializerMixin):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    seasons = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))

    serialize_rules = ('-service.shows',)

    def __repr__(self):
        return f'<Show Name: {self.name}, seasons: {self.seasons}>'