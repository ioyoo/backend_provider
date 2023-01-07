from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from .data.credentials import DBCredentials
import json

app = Flask(__name__)
cred = DBCredentials()
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{cred.USER}:{cred.PASS}@{cred.URL}:{cred.PORT}/{cred.DB_NAME}'
db = SQLAlchemy(app)
api = Api(app)

users = [{"name": "me"}, {"name": "mantas", "counter": 3123513471}]
id = 0


class Stock(db.Model):
    __tablename__ = "stock"

    name = db.Column('name', db.String(100), primary_key=True)
    score = db.Column(db.Float)

    def __init__(self, name, score):
        self.name = name
        self.score = score

    @property
    def serialize(self):
        return {
            'name': self.name,
            'score': self.score
        }


class StockList(Resource):
    def get(self):
        return jsonify(json_list=[item.serialize for item in db.session.query(Stock).all()])


class StockCreate(Resource):
    def get(self):
        db.create_all()


api.add_resource(StockList, "/stocks")
api.add_resource(StockCreate, "/create")
