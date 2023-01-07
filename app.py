from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from .data.credentials import DBCredentials
import json

app = Flask(__name__)
cred = DBCredentials()
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{cred.USER}:{cred.PASS}@{cred.URL}:{cred.PORT}/{cred.DB_NAME}'
db = SQLAlchemy(app)
api = Api(app)


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
        return jsonify([item.serialize for item in db.session.query(Stock).all()])

    def post(self):
        stock_json: dict = json.loads(request.get_json(force=True))
        for name, score in stock_json.items():
            stock = Stock(name, score)
            db.session.add(stock)
            db.session.commit()
            app.logger.info(f"Introduced {name} : {score} in table")


api.add_resource(StockList, "/api/stocks")
