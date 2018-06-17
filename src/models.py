from app import app, db
from datetime import datetime


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.Integer, nullable=False)
    consumption = db.Column(db.String(250), nullable=False)
    color = db.Column(db.String(250), nullable=False)
    miles = db.Column(db.Integer, nullable=False, default=0)
    category = db.Column(db.String(250), nullable=False)
    photo = db.Column(db.String(250), nullable=False)
    user = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    @property
    def serialize(self):
    # Return object data in easily serializable format
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'year': self.year,
            'fuel': self.fuel,
            'consumption': self.consumption,
            'color': self.color,
            'img_url': self.photo,
            'date': self.date
        }
